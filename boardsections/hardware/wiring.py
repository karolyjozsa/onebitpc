"""Connection of HW elements simulated by Qt signals"""

from collections.abc import Callable
from PySide6 import QtCore

from typedefinitions import TTL


class Wire(QtCore.QObject):
    """A wire from an output to input(s)"""
    level_changed = QtCore.Signal((TTL,))

    def solder_to(self, input: Callable[[TTL], None]) -> None:
        self.level_changed.connect(input)

    def output_changed(self, new_value: TTL) -> None:
        self.level_changed.emit(new_value)
