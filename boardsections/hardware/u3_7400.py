"""Simulate the 7400 IC"""

from boardsections.hardware.wiring import Wire
from typedefinitions import TTL

def nand(inp1: TTL, inp2: TTL) -> TTL:
    """One NAND gate in the IC"""
    return ~(inp1 & inp2)

class Nand:
    def __init__(self, output: Wire) -> None:
        self.input1_value = TTL.L
        self.input2_value = TTL.L
        self.output = output

    def input1(self, new_value: TTL):
        self.input1_value = new_value
        self._input_changed()

    def input2(self, new_value: TTL):
        self.input2_value = new_value
        self._input_changed()

    def _input_changed(self):
        output_value = ~(self.input1_value & self.input2_value)
        self.output.emit(output_value)

