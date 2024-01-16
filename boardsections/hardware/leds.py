"""Simulate the LEDs"""

from PySide6 import QtCore

from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL


@hw_elem
class Led:
    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
        self.voltage: float = 0.2

    def _display(self) -> None:
        print(f'{self.name} LED is {"ON" if self.voltage > 4.2 else "OFF"}')

    @input
    @QtCore.Slot(TTL)
    def anode(self, input: TTL) -> None:
        self.voltage = input.voltage()
        self._display()
