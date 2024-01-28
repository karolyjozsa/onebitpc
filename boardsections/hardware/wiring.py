"""Connections of HW elements simulated by Qt signals and slots

A HW element has input(s) and output(s). E.g. a NAND gate has 2x inputs and 1x
output.

Outputs are Wire objects. The change of voltage event on the wire is simulated
by Qt signals. Output objects can be "soldered" to inputs, which are simulated
by Qt slots. Soldering creates the connection from an output to input(s).

When the output changes, it emits a signal. All connected input slots are then
executed. The triggered elements calculate their outputs and if there is a
change emit their signals, and so on.
"""

from collections.abc import Callable
import logging
import math
from PySide6.QtCore import QObject, Signal

from tools import wiring_checker
from typedefinitions import TTL, Voltage


# Whether voltage wire is the default
ANALOGUE_BY_DEFAULT = False


def volt_to_ttl(input: Callable[[TTL], None]) -> Callable[[Voltage], None]:
    """Replace a TTL input with an analogue input"""
    def converter(value: Voltage) -> None:
        input(value.to_ttl)
    return converter

def ttl_to_volt(input: Callable[[Voltage], None]) -> Callable[[TTL], None]:
    """Replace an analogue input with a TTL input"""
    def converter(value: TTL) -> None:
        input(value.to_volt)
    return converter


class Wire(QObject):
    """A wire from an output to input(s)"""
    level_changed_volt = Signal((Voltage,))
    level_changed_ttl = Signal((TTL,))

    def __init__(self,
                 name: str,
                 analogue: bool = ANALOGUE_BY_DEFAULT
    ) -> None:
        super().__init__(None)
        self.name = name
        self.analogue = analogue
        if analogue:
            self.current_level: Voltage = Voltage(0.0)
        else:
            self.current_level: TTL = TTL.L

    def solder_to(self,
                  input: Callable[[TTL | Voltage], None],
                  analogue: bool = ANALOGUE_BY_DEFAULT
    ) -> None:
        """Connect an output to an input"""
        wiring_checker.input_connected(input)
        if self.analogue:
            if analogue:
                # analogue wire to analogue input
                self.level_changed_volt.connect(input)
            else:
                # analogue wire to TTL input
                self.level_changed_volt.connect(volt_to_ttl(input))
        else:
            if analogue:
                # TTL wire to analogue input
                self.level_changed_ttl.connect(ttl_to_volt(input))
            else:
                # TTL wire to TTL input
                self.level_changed_ttl.connect(input)

    def set_output_level(self, new_value: TTL | Voltage) -> None:
        """Set the voltage or TTL level on the wire
        
        The wire level is what the output defines. HW elements can set the
        same level multiple times, but the connected inputs only receive the
        related signal when this level is not the same as the previous one.
        """
        assert type(new_value) is Voltage if self.analogue else TTL
        if self.current_level != new_value:
            logging.info(f"{self.name} -> {new_value}")
            self.current_level = new_value
            if self.analogue:
                self.level_changed_volt.emit(new_value)
            else:
                self.level_changed_ttl.emit(new_value)
