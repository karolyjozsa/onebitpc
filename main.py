"""Run the 1-bit computer"""

import asyncio

from boardsections.clock import AstableMultivibrator
from boardsections.cpu import ProgCounter, Register
from boardsections.hardware.dipswitches import DipSwitch
from boardsections.rom import Program
from typedefinitions import TTL


def clock_change(clock_level: TTL) -> None:
    """Callback for triggering TTL changes on clock"""
    # Positive-going edge triggers CPU instruction
    if clock_level == TTL.H:
        register.set_output()
        prog_counter.set_output()

# Instantiate clock generator and simulated resources
clock_gen = AstableMultivibrator(clock_change)
rom_program = Program()
register = Register(rom_program)
prog_counter = ProgCounter(rom_program)

# Set the program code
rom_program.programming([
    DipSwitch(0, 0),  # XOR 0
    DipSwitch(0, 1),  # XOR 1
])

asyncio.run(clock_gen.run())
