"""CPU sections on the board

The sections inside the CPU usually are
- CPU internal memory/register (implemented by a FlipFlop)
- CPU program counter store (implemented by a FlipFlop)
- Arithmetic Logic Unit to calculate register value (implemented by a
  Multiplexer)
- Program counter calcultator (implemented by a Multiplexer)
- An XOR calculation section to implement an XOR gate
"""

from PySide6 import QtCore

from boardsections.hardware.psu import GROUND, VCC
from boardsections.hardware.u2_7474 import FlipFlop
from boardsections.hardware.u3_7400 import Nand
from boardsections.hardware.u4_74153 import Multiplexer
from boardsections.hardware.wiring import Wire
from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL


class Register(FlipFlop):
    """CPU internal memory/register"""
    def __init__(self) -> None:
        super().__init__("register")
        VCC.solder_to(self.preset_inv)
        VCC.solder_to(self.clear_inv)


class PrgCnt(FlipFlop):
    """CPU program counter store"""
    def __init__(self) -> None:
        super().__init__("prog_cnt")
        VCC.solder_to(self.preset_inv)
        VCC.solder_to(self.clear_inv)


class Alu:
    """The Arithmetic Logic Unit"""
    def __init__(self) -> None:
        self.mux = Multiplexer("alu")
        GROUND.solder_to(self.mux.data2)
        GROUND.solder_to(self.mux.data3)
        GROUND.solder_to(self.mux.enable_inv)
        GROUND.solder_to(self.mux.select1)


class PrgCntCalc:
    """The program code address pointer calculator"""
    def __init__(self) -> None:
        self.mux = Multiplexer("prog_cnt_calc")
        GROUND.solder_to(self.mux.data2)
        GROUND.solder_to(self.mux.data3)
        GROUND.solder_to(self.mux.enable_inv)
        GROUND.solder_to(self.mux.select1)


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

        # Virtual wiring of the XOR inputs to the NAND gates
        self.input1_emitter = Wire("xor_input1_emitter")
        self.input2_emitter = Wire("xor_input2_emitter")
        self.input1_emitter.solder_to(self.nand1.input1)
        self.input1_emitter.solder_to(self.nand2.input1)
        self.input2_emitter.solder_to(self.nand1.input2)
        self.input2_emitter.solder_to(self.nand3.input2)

    @input
    @QtCore.Slot(TTL)
    def input1(self, new_value: TTL):
        self.input1_emitter.set_output_level(new_value)

    @input
    @QtCore.Slot(TTL)
    def input2(self, new_value: TTL):
        self.input2_emitter.set_output_level(new_value)
