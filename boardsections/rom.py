"""ROM section on the board"""

from enum import Enum

from boardsections.hardware.wiring import Wire
from typedefinitions import TTL
from boardsections.hardware.dipswitches import DipSwitch, dip_switch_array


class InstrunctionMnemonic(Enum):
    XOR = 0  # Execute an XOR of the register and the instruction data,
             # then step the program counter to the next address.
    JMP = 1  # Jump, i.e. set the program counter to the address stated
             # by the instruction data. The register does not change.


class Rom:
    """The program code "burnt" into the ROM
    
    The actual data is stored in the dip switch HW. This class:
    - reads program code from dip switches by the program counter
    - can burn code content (simulating setting dip switches)
    - can provide verbose code
    """
    program_counter0: TTL

    def __init__(self, output_data: Wire, output_address: Wire) -> None:
        self.address_value: TTL = TTL.L
        self.output_data = output_data
        self.output_address = output_address
    
    def address(self, new_value: TTL) -> None:
        """Slot: address changed"""
        if self.address_value == new_value:
            return

        self.address_value = new_value
        dipswitch: DipSwitch = dip_switch_array[new_value.value]
        self.output_data.changes_to(TTL(dipswitch.switch_one))
        self.output_address.changes_to(TTL(dipswitch.switch_two))

    @staticmethod
    def programming(new_codes: list[DipSwitch]) -> None:
        """Set the code in the dip switches"""
        for address in range(len(dip_switch_array)):
            dip_switch_array[address] = new_codes[address]

    def get_verbose_instruction(self) -> str:
        """Returns a readable code, e.g. 'XOR 1'"""
        code = dip_switch_array[self.address_value.value]
        mnemonic = InstrunctionMnemonic(code.switch_one).name
        instr_data = code.switch_two
        return f'{mnemonic} {instr_data}'
