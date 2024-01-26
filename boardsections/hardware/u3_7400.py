"""Simulate the 7400 quad NAND IC"""

from PySide6 import QtCore

from boardsections.hardware.psu import Vcc
from boardsections.hardware.wiring import Wire
from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL

@hw_elem
class Nand:
    def __init__(self, name: str) -> None:
        self.powered = False
        Vcc().solder_to(self.vcc)
        self.input1_value = TTL.L
        self.input2_value = TTL.L
        self.output = Wire(f"{name}_out")

    @input
    @QtCore.Slot(TTL)
    def vcc(self, power: TTL) -> None:
        self.powered = power == TTL.H

    @input
    @QtCore.Slot(TTL)
    def input1(self, new_value: TTL) -> None:
        self.input1_value = new_value
        self._input_changed()

    @input
    @QtCore.Slot(TTL)
    def input2(self, new_value: TTL) -> None:
        self.input2_value = new_value
        self._input_changed()

    def _input_changed(self) -> None:
        output_value = ~(self.input1_value & self.input2_value)
        if self.powered:
            self.output.set_output_level(output_value)
