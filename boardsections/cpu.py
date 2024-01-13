"""CPU section on the board

- A 1-bit register containing memory (FlipFlop) and an LED
- A 1-bit program counter (FlipFlop) and an LED
- An XOR calculation section
"""

from PySide6 import QtCore

from boardsections.hardware.u3_7400 import Nand
from boardsections.hardware.u4_74153 import Multiplexer
from boardsections.hardware.wiring import Wire
from typedefinitions import TTL


class Alu:
    """The Arithmetic Logic Unit in the CPU"""
    def __init__(self) -> None:
        self.mux = Multiplexer(Wire())
        self.mux.data2(TTL.L)
        self.mux.data3(TTL.L)
        self.mux.enable_inv(TTL.L)
        self.mux.select1(TTL.L)


class AddrPtr:
    """The CPU program code address pointer"""
    def __init__(self) -> None:
        self.mux = Multiplexer(Wire())
        self.mux.data2(TTL.L)
        self.mux.data3(TTL.L)
        self.mux.enable_inv(TTL.L)
        self.mux.select1(TTL.L)


class Xor(QtCore.QObject):
    """An XOR logic by wired 4x NAND gates"""
    def __init__(self, output: Wire) -> None:
        self.in1_internal = Wire()
        self.in2_internal = Wire()
        self.nand1 = Nand(Wire())
        self.nand2 = Nand(Wire())
        self.nand3 = Nand(Wire())
        nand4 = Nand(output)
        self.output = output

        # Internal wiring of NAND gates
        self.in1_internal.solder_to(self.nand1.input1)
        self.in1_internal.solder_to(self.nand2.input1)
        self.in2_internal.solder_to(self.nand1.input2)
        self.in2_internal.solder_to(self.nand3.input2)
        self.nand1.output.solder_to(self.nand2.input2)
        self.nand1.output.solder_to(self.nand3.input1)
        self.nand2.output.solder_to(nand4.input1)
        self.nand3.output.solder_to(nand4.input2)

    def input1(self, new_value: TTL):
        """Slot: input1 changed"""
        self.in1_internal.changes_to(new_value)

    def input2(self, new_value: TTL):
        """Slot: input2 changed"""
        self.in2_internal.changes_to(new_value)
