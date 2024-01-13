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
from PySide6 import QtCore

from typedefinitions import TTL


class Wire(QtCore.QObject):
    """A wire from an output to input(s)"""
    level_changed = QtCore.Signal((TTL,))

    def solder_to(self, input: Callable[[TTL], None]) -> None:
        """Connec an output to an input"""
        self.level_changed.connect(input)

    def changes_to(self, new_value: TTL) -> None:
        self.level_changed.emit(new_value)
