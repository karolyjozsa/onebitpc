"""Simulate the 7400 quad NAND IC"""

import logging

from PySide6 import QtCore

from boardsections.hardware.psu import PSU
from boardsections.hardware.wiring import Wire
from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL

@hw_elem
class Nand:
    powered: bool = False

    def __init__(self, name: str) -> None:
        PSU.vcc.solder_to(self.vcc)
        self.name = name
        self.input1_value = TTL.L
        self.input2_value = TTL.L
        self.output = Wire(f"{name}_out")

    @input
    @QtCore.Slot(TTL)
    def vcc(self, power: TTL) -> None:
        self.powered = power == TTL.H
        logging.info(f"{self.name} {self.powered=}")
        self._output_changes()

    @input
    @QtCore.Slot(TTL)
    def input1(self, new_value: TTL) -> None:
        self.input1_value = new_value
        self._output_changes()

    @input
    @QtCore.Slot(TTL)
    def input2(self, new_value: TTL) -> None:
        self.input2_value = new_value
        self._output_changes()

    def _output_changes(self) -> None:
        output_value = ~(self.input1_value & self.input2_value)
        if self.powered:
            self.output.set_output_level(output_value)
