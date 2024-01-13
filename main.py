"""The 1-bit computer simulation

Create and connect the board sections, i.e. HW elements or logical blocks:

- ROM
- Clock
- CPU register (memory)
- CPU program counter storage
- An arithmetic processor (a multiplexer) setting the Register
- A program counter calculator (a multiplexer) setting the ProgCounter
- LEDs
- Reset button
"""

import asyncio

from boardsections.clock import AstableMultivibrator
from boardsections.cpu import Alu, AddrPtr, Xor
from boardsections.hardware.dipswitches import DipSwitch
from boardsections.hardware.leds import ClockLed, ProgCountLed, RegisterLed
from boardsections.hardware.u2_7474 import FlipFlop
from boardsections.hardware.wiring import Wire
from boardsections.rom import Rom


####################################
## Create simulated elements
####################################

# Reset button
# ??????

# LEDs
register_led = RegisterLed()
pc_led = ProgCountLed()
clock_led = ClockLed()

# Complex sections
clock = AstableMultivibrator(Wire())
rom = Rom(Wire(), Wire())
register = FlipFlop(Wire(), Wire())
prog_cnt = FlipFlop(Wire(), Wire())

# Create calculating sections
xor = Xor(Wire())
alu = Alu()
addr_ptr = AddrPtr()


####################################
## Solder outputs to other elements
####################################

# Clock to Register, ProgCounter and LED
clock.output.solder_to(register.clock)
clock.output.solder_to(prog_cnt.clock)
clock.output.solder_to(clock_led.anode)

# Register to XOR, ALU and LED
register.output_q.solder_to(xor.input1)
register.output_q.solder_to(alu.mux.data1)
register.output_q.solder_to(register_led.anode)

# Program Counter to ROM, Addres Pointer and LED
prog_cnt.output_q.solder_to(rom.address)
prog_cnt.output_q_inv.solder_to(addr_ptr.mux.data0)
prog_cnt.output_q.solder_to(pc_led.anode)

# ROM to arithmetic and addressing sections
rom.output_data.solder_to(xor.input2)
rom.output_data.solder_to(addr_ptr.mux.data1)
rom.output_address.solder_to(alu.mux.select0)
rom.output_address.solder_to(addr_ptr.mux.select0)

# XOR to ALU
xor.output.solder_to(alu.mux.data0)

# ALU to Register
alu.mux.output.solder_to(register.data)

# Addres Pointer to ProgCounter
addr_ptr.mux.output.solder_to(prog_cnt.data)


####################################
## Set the program code
####################################
rom.programming([
    DipSwitch(0, 0),  # XOR 0
    DipSwitch(0, 1),  # XOR 1
])

####################################
## Run the simulation
####################################
asyncio.run(clock.run())
