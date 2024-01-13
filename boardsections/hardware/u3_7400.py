"""Simulate the 7400 quad NAND IC"""

from boardsections.hardware.wiring import Wire
from typedefinitions import TTL

class Nand:
    def __init__(self, output: Wire) -> None:
        self.input1_value = TTL.L
        self.input2_value = TTL.L
        self.output = output

    def input1(self, new_value: TTL) -> None:
        self.input1_value = new_value
        self._input_changed()

    def input2(self, new_value: TTL) -> None:
        self.input2_value = new_value
        self._input_changed()

    def _input_changed(self) -> None:
        output_value = ~(self.input1_value & self.input2_value)
        self.output.changes_to(output_value)

