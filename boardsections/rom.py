"""ROM functions"""

from enum import Enum

from typedefinitions import Bit, TTL
from boardsections.hardware.dipswitches import DipSwitch, dip_switch_array


class InstrunctionMnemonic(Enum):
    XOR = 0  # Execute an XOR of the register and the instruction data,
             # then step the program counter to the next address.
    JMP = 1  # Jump, i.e. set the program counter to the address stated
             # by the instruction data. The register does not change.


class Program:
    """The program code "burnt" into the ROM
    
    The actual data is stored in the dip switch HW. This class:
    - maintains the program counter
    - reads program code from dip switches
    - can burn code content (simulating setting dip switches)
    """
    program_counter0: TTL

    def __init__(self) -> None:
        self.set_address(TTL(0))

    def set_address(self, program_counter0: TTL) -> None:
        self.program_counter0 = program_counter0

    def get_code(self) -> tuple[TTL, TTL]:
        dipswitch = dip_switch_array[self.program_counter0.value]
        return (TTL(dipswitch.switch_one), TTL(dipswitch.switch_two))

    @staticmethod
    def programming(new_codes: list[DipSwitch]) -> None:
        for address in range(len(dip_switch_array)):
            dip_switch_array[address] = new_codes[address]

    def get_verbose_instruction(self) -> str:
        """Returns a readable code, e.g. 'XOR 1'"""
        code = self.get_code()
        mnemonic = InstrunctionMnemonic(code[0].value).name
        instr_data = code[1].value
        return f'{mnemonic} {instr_data}'
