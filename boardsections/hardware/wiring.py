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
from PySide6.QtCore import QObject, Signal

from tools import wiring_checker
from typedefinitions import TTL


class Wire(QObject):
    """A wire from an output to input(s)"""
    level_changed = Signal((TTL,))

    def __init__(self, name: str) -> None:
        super().__init__(None)
        self.name = name
        self.current_ttl = TTL.L

    def solder_to(self, input: Callable[[TTL], None]) -> None:
        """Connec an output to an input"""
        wiring_checker.input_connected(input)
        self.level_changed.connect(input)

    def set_output_level(self, new_value: TTL) -> None:
        if self.current_ttl != new_value:
            self.current_ttl = new_value
            self.level_changed.emit(new_value)


class FixedWire:
    """Special HW element, i.e. fix wiring to ground or Vcc
    
    When an input is soldered to the ground, it automatically sent a signal
    with LOW. Vcc sends a signal with HIGH.
    """
    def __init__(self, fixlevel: TTL) -> None:
        self.output = Wire(str(fixlevel))
        self.fixlevel = fixlevel
        # Store the original solder_to()
        self.wire_solder_to_input = self.output.solder_to
        self.output.solder_to = self.ground_soldered_to_input
    
    def ground_soldered_to_input(self, input: Callable[[TTL], None]) -> None:
        """This replaces the original solder_to() to also sends signal"""
        self.wire_solder_to_input(input)
        self.output.set_output_level(self.fixlevel)
