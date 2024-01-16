"""Simulate the 74153 dual 4-to-1 multiplexer IC"""

from PySide6 import QtCore

from boardsections.hardware.wiring import Wire
from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL


SELECT_BIT_MASK = [0b01, 0b10]


@hw_elem
class Multiplexer:
    def __init__(self, name: str) -> None:
        self.data_values: list[TTL] = [TTL.L for _ in range(4)]
        self.enable_inv_value: TTL = TTL.L
        self.select: int = 0*SELECT_BIT_MASK[0] + 0*SELECT_BIT_MASK[1]
        self.output = Wire(f"{name}_out")

    @input
    @QtCore.Slot(TTL)
    def data0(self, new_value: TTL) -> None:
        """Slot: data0 changed"""
        self._data(0, new_value)

    @input
    @QtCore.Slot(TTL)
    def data1(self, new_value: TTL) -> None:
        """Slot: data1 changed"""
        self._data(1, new_value)

    @input
    @QtCore.Slot(TTL)
    def data2(self, new_value: TTL) -> None:
        """Slot: data2 changed"""
        self._data(2, new_value)

    @input
    @QtCore.Slot(TTL)
    def data3(self, new_value: TTL) -> None:
        """Slot: data3 changed"""
        self._data(3, new_value)
    
    def _data(self, idx, new_value) -> None:
        self.data_values[idx] = new_value
        if ~self.enable_inv_value and self.select == idx:
            self.output.set_output_level(new_value)

    @input
    @QtCore.Slot(TTL)
    def select0(self, new_value: TTL) -> None:
        """Slot: select0 changed"""
        self._select(0, new_value)

    @input
    @QtCore.Slot(TTL)
    def select1(self, new_value: TTL) -> None:
        """Slot: select1 changed"""
        self._select(1, new_value)
    
    def _select(self, select_bit, new_value) -> None:
        self.select = (
            new_value.value*SELECT_BIT_MASK[select_bit] +
            self.select&SELECT_BIT_MASK[~select_bit]
        )
        if ~self.enable_inv_value:
            self.output.set_output_level(self.data_values[self.select])

    @input
    @QtCore.Slot(TTL)
    def enable_inv(self, new_value) -> None:
        """Slot: enable_inv changed"""
        self.enable_inv_value = new_value
        # Output only changes if the actual data is HIGH
        if self.data_values[self.select] == TTL.H:
            # Enabling data out?
            if new_value == TTL.L:
                self.output.set_output_level(self.data_values[self.select])
            else:
                self.output.set_output_level(TTL.L)
