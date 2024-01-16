"""Simulate the 7414 6x Schmidt-Trigger IC"""

from PySide6 import QtCore

from boardsections.hardware.wiring import Wire
from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL


THRESHOLD_HIGH = 4.2
THRESHOLD_LOW = 0.6


@hw_elem
class SchmidtTrigger:
    def __init__(self, name: str) -> None:
        self.output_value: TTL = TTL.L
        self.output = Wire(f"{name}_out")
    
    @input
    @QtCore.Slot(TTL)
    def input(self, new_value: float | TTL) -> None:
        if isinstance(new_value, TTL):
            self.output.set_output_level(new_value)
            return

        if new_value > THRESHOLD_HIGH and self.output_value == TTL.L:
            self.output_value = TTL.H
            self.output.set_output_level(self.output_value)

        if new_value < THRESHOLD_LOW and self.output_value == TTL.H:
            self.output_value = TTL.L
            self.output.set_output_level(self.output_value)
