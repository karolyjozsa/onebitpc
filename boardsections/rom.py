"""ROM section on the board"""

from enum import Enum

from PySide6 import QtCore

from boardsections.hardware.dipswitches import DipSwitch, dip_switch_array
from boardsections.hardware.wiring import Wire
from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL


class InstrunctionMnemonic(Enum):
    XOR = 0  # Execute an XOR of the register and the instruction data,
             # then step the program counter to the next address.
    JMP = 1  # Jump, i.e. set the program counter to the address stated
             # by the instruction data. The register does not change.


@hw_elem
class Rom:
    """The program code "burnt" into the ROM
    
    The actual data is stored in the dip switch HW. This class:
    - reads program code from dip switches by the program counter
    - can burn code content (simulating setting dip switches)
    - can provide verbose code
    """
    def __init__(self) -> None:
        self.address_value: TTL = TTL.L
        self.output_data = Wire("rom_out_data")
        self.output_address = Wire("rom_out_address")
    
    @input
    @QtCore.Slot(TTL)
    def address(self, new_value: TTL) -> None:
        """Slot: address changed"""
        self.address_value = new_value
        dipswitch: DipSwitch = dip_switch_array[new_value.value]
        self.output_address.set_output_level(TTL(dipswitch.switch_one))
        self.output_data.set_output_level(TTL(dipswitch.switch_two))

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
