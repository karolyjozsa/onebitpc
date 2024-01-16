"""CPU section on the board

- A 1-bit register containing memory (FlipFlop) and an LED
- A 1-bit program counter (FlipFlop) and an LED
- An XOR calculation section
"""

from PySide6 import QtCore

from boardsections.hardware.u3_7400 import Nand
from boardsections.hardware.u4_74153 import Multiplexer
from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL


class Alu:
    """The Arithmetic Logic Unit in the CPU"""
    def __init__(self) -> None:
        self.mux = Multiplexer("alu")
        self.mux.data2(TTL.L)
        self.mux.data3(TTL.L)
        self.mux.enable_inv(TTL.L)
        self.mux.select1(TTL.L)


class AddrPtr:
    """The CPU program code address pointer"""
    def __init__(self) -> None:
        self.mux = Multiplexer("addrptr")
        self.mux.data2(TTL.L)
        self.mux.data3(TTL.L)
        self.mux.enable_inv(TTL.L)
        self.mux.select1(TTL.L)


@hw_elem
class Xor():
    """An XOR logic by wired 4x NAND gates"""
    def __init__(self) -> None:
        self.nand1 = Nand("nand1")
        self.nand2 = Nand("nand2")
        self.nand3 = Nand("nand3")
        self.nand4 = Nand("nand4")
        self.output = self.nand4.output

        # Internal wiring of NAND gates
        self.nand1.output.solder_to(self.nand2.input2)
        self.nand1.output.solder_to(self.nand3.input1)
        self.nand2.output.solder_to(self.nand4.input1)
        self.nand3.output.solder_to(self.nand4.input2)

    @input
    @QtCore.Slot(TTL)
    def input1(self, new_value: TTL):
        self.nand1.input1(new_value)
        self.nand2.input1(new_value)

    @input
    @QtCore.Slot(TTL)
    def input2(self, new_value: TTL):
        self.nand1.input2(new_value)
        self.nand3.input2(new_value)
