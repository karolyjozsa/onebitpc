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
        logging.info(f"{self.name} -> {new_value} while {self.current_ttl=}")
        if self.current_ttl != new_value:
            self.current_ttl = new_value
            self.level_changed.emit(new_value)
