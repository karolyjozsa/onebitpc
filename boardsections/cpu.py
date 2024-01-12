"""CPU functions"""

from boardsections.hardware.leds import ProgCountLed, RegisterLed
from boardsections.rom import Program
from boardsections.hardware.u2_7474 import FlipFlop
from boardsections.hardware.u3_7400 import nand
from boardsections.hardware.u4_74153 import multiplexer
from typedefinitions import TTL


class Register(FlipFlop):
    """The CPU register (internal memory)"""
    def __init__(self, rom_program: Program) -> None:
        self.rom_program = rom_program
        self.register_led = RegisterLed()
        super().__init__()  # this calls the output_changed()

    def output_changed(self) -> None:
        """Called when output changes on the Register flip-flop output"""
        self.register_led.set_voltage(self.q_output.voltage())

        new_register_value = data_processing(
            rom_program=self.rom_program,
            register=self.q_output
        )
        self.data = new_register_value
        print(f'{new_register_value=}')


class ProgCounter(FlipFlop):
    def __init__(self, rom_program: Program) -> None:
        self.rom_program = rom_program
        self.pc_led = ProgCountLed()
        super().__init__()  # this calls the output_changed()

    def output_changed(self) -> None:
        """Called when output changes on the ProgCounter flip-flop output"""
        self.rom_program.set_address(self.q_output)
        self.pc_led.set_voltage(self.q_output.voltage())
        
        new_address_value = address_processing(
            rom_program=self.rom_program,
            progcounter_inv=self.q_inv_output
        )
        self.data = new_address_value


def xor_block(inp1: TTL, inp2: TTL) -> TTL:
    """The 4x NAND gates of the IC implement an XOR function"""
    gate_a_out = nand(inp1, inp2)
    gate_b_out = nand(inp1, gate_a_out)
    gate_c_out = nand(gate_a_out, inp2)
    gate_d_out = nand(gate_b_out, gate_c_out)
    return gate_d_out


def data_processing(rom_program: Program, register: TTL) -> TTL:
    """Execute a CPU instruction to calculate data"""
    rom_code = rom_program.get_code()
    xor_result = xor_block(register, rom_code[1])
    print(f'{rom_code=}, {xor_result=}')
    result_data = multiplexer(
        data0=xor_result,
        data1=register,
        data2=TTL.L,
        data3=TTL.L,
        enable_inv=TTL.L,
        select0=rom_code[0],
        select1=TTL.L
    )
    return result_data


def address_processing(rom_program: Program, progcounter_inv: TTL) -> TTL:
    """Execute a CPU instruction to calculate program counter"""
    rom_code = rom_program.get_code()
    result_address = multiplexer(
        data0=progcounter_inv,
        data1=rom_code[1],
        data2=TTL.L,
        data3=TTL.L,
        enable_inv=TTL.L,
        select0=rom_code[0],
        select1=TTL.L
    )
    return result_address
