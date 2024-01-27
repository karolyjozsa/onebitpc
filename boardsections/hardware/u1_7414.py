"""Simulate the 7414 6x Schmidt-Trigger IC"""

import logging

from PySide6 import QtCore

from boardsections.hardware.psu import PSU
from boardsections.hardware.wiring import Wire
from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL


THRESHOLD_HIGH = 4.2
THRESHOLD_LOW = 0.6


@hw_elem
class SchmidtTrigger:
    powered: bool = False

    def __init__(self, name: str) -> None:
        PSU.vcc.solder_to(self.vcc)
        self.name = name
        self.output_value: TTL = TTL.L
        self.output = Wire(f"{name}_out")

    @input
    @QtCore.Slot(TTL)
    def vcc(self, power: TTL) -> None:
        self.powered = power == TTL.H
        logging.info(f"{self.name} {self.powered=}")
        self._output_changes()
    
    @input
    @QtCore.Slot(TTL)
    def input(self, new_value: float | TTL) -> None:
        if isinstance(new_value, TTL):
            self.output_value = new_value
            self._output_changes()
            return

        if new_value > THRESHOLD_HIGH and self.output_value == TTL.L:
            self.output_value = TTL.H
        elif new_value < THRESHOLD_LOW and self.output_value == TTL.H:
            self.output_value = TTL.L
        else:
            return

        self._output_changes()

    def _output_changes(self) -> None:
        if self.powered:
            self.output.set_output_level(self.output_value)
