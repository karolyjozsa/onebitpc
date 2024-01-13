"""Simulate the 74153 dual 4-to-1 multiplexer IC"""

from boardsections.hardware.wiring import Wire
from typedefinitions import TTL


SELECT_BIT_MASK = [0b01, 0b10]


class Multiplexer:
    def __init__(self, output: Wire) -> None:
        self.data_value: list[TTL] = [TTL.L for _ in range(4)]
        self.enable_inv_value: TTL = TTL.L
        self.select: int = 0*SELECT_BIT_MASK[0] + 0*SELECT_BIT_MASK[1]
        self.output = output

    def data0(self, new_value: TTL) -> None:
        self._data(0, new_value)

    def data1(self, new_value: TTL) -> None:
        self._data(1, new_value)

    def data2(self, new_value: TTL) -> None:
        self._data(2, new_value)

    def data3(self, new_value: TTL) -> None:
        self._data(3, new_value)
    
    def _data(self, idx, new_value) -> None:
        if self.data_value[idx] == new_value:
            return
        self.data_value[idx] = new_value
        if ~self.enable_inv_value and self.select == idx:
            self.output.changes_to(new_value)

    def select0(self, new_value: TTL) -> None:
        self._select(0, new_value)

    def select1(self, new_value: TTL) -> None:
        self._select(1, new_value)
    
    def _select(self, select_bit, new_value) -> None:
        if self.select&SELECT_BIT_MASK[select_bit] == new_value.value:
            return
        self.select = (
            new_value.value*SELECT_BIT_MASK[select_bit] +
            self.select&SELECT_BIT_MASK[~select_bit]
        )
        if ~self.enable_inv_value:
            self.output.changes_to(self.data_value[self.select])

    def enable_inv(self, new_value) -> None:
        if self.enable_inv_value == new_value:
            return
        self.enable_inv_value = new_value
        # Output only changes if the actual data is HIGH
        if self.data_value[self.select] == TTL.H:
            # Enabling data out?
            if new_value == TTL.L:
                self.output.changes_to(self.data_value[self.select])
            else:
                self.output.changes_to(TTL.L)
