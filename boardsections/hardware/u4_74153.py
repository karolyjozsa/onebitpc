"""Simulate the 74153 dual 4-to-1 multiplexer IC"""

import logging

from PySide6 import QtCore

from boardsections.hardware.psu import PSU
from boardsections.hardware.wiring import Wire
from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL


SELECT_BIT_MASK = [0b01, 0b10]


@hw_elem
class Multiplexer:
    powered: bool = False

    def __init__(self, name: str) -> None:
        PSU.vcc.solder_to(self.vcc)
        self.name = name
        self.data_values: list[TTL] = [TTL.L for _ in range(4)]
        self.enable_inv_value: TTL = TTL.L
        self.select: int = 0*SELECT_BIT_MASK[0] + 0*SELECT_BIT_MASK[1]
        self.output = Wire(f"{name}_out")
        self.output_value: TTL = TTL.L

    @input
    @QtCore.Slot(TTL)
    def vcc(self, power: TTL) -> None:
        self.powered = power == TTL.H
        logging.info(f"{self.name} {self.powered=}")
        self._output_changes()

    @input
    @QtCore.Slot(TTL)
    def data0(self, new_value: TTL) -> None:
        self._data(0, new_value)

    @input
    @QtCore.Slot(TTL)
    def data1(self, new_value: TTL) -> None:
        self._data(1, new_value)

    @input
    @QtCore.Slot(TTL)
    def data2(self, new_value: TTL) -> None:
        self._data(2, new_value)

    @input
    @QtCore.Slot(TTL)
    def data3(self, new_value: TTL) -> None:
        self._data(3, new_value)
    
    def _data(self, idx, new_value) -> None:
        self.data_values[idx] = new_value
        if ~self.enable_inv_value and self.select == idx:
            self.output_value = new_value
            self._output_changes()

    @input
    @QtCore.Slot(TTL)
    def select0(self, new_value: TTL) -> None:
        self._select(0, new_value)

    @input
    @QtCore.Slot(TTL)
    def select1(self, new_value: TTL) -> None:
        self._select(1, new_value)
    
    def _select(self, select_bit, new_value) -> None:
        self.select = (
            new_value.value*SELECT_BIT_MASK[select_bit] +
            self.select&SELECT_BIT_MASK[~select_bit]
        )
        if ~self.enable_inv_value:
            self.output_value = self.data_values[self.select]
            self._output_changes()

    @input
    @QtCore.Slot(TTL)
    def enable_inv(self, new_value) -> None:
        self.enable_inv_value = new_value
        # Output only changes if the actual data is HIGH
        if self.data_values[self.select] == TTL.H:
            # Enabling data out?
            if new_value == TTL.L:
                self.output_value = self.data_values[self.select]
            else:
                self.output_value = TTL.L
            self._output_changes()

    def _output_changes(self) -> None:
        if self.powered:
            self.output.set_output_level(self.output_value)
