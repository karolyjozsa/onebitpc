"""The 1-bit computer simulation

The physical board contains ICs and other HW elements. This code aims to
simulate these HW elements and their connection (wiring).

Atomic elements are collected into logical blocks.
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
from boardsections.cpu import Alu, PrgCnt, PrgCntCalc, Register, Xor
from boardsections.hardware.psu import VCC
from boardsections.hardware.dipswitches import DipSwitch
from boardsections.hardware.leds import Led
from boardsections.rom import Rom
from tools import wiring_checker


####################################
## Create simulated elements
####################################

# Power switch and Reset button
# ??????

# LEDs
power_led = Led('Pwr', 'white')
VCC.solder_to(power_led.anode)
register_led = Led('Reg', 'red')
pc_led = Led('PC', 'yellow')
clock_led = Led('Clock', 'blue')

# CPU sections
register = Register()
prog_cnt = PrgCnt()
xor = Xor()
alu = Alu()
prog_cnt_calc = PrgCntCalc()

# Other computer HW sections
clock = AstableMultivibrator()
rom = Rom()

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
prog_cnt.output_q_inv.solder_to(prog_cnt_calc.mux.data0)
prog_cnt.output_q.solder_to(pc_led.anode)

# ROM to arithmetic and addressing sections
rom.output_data.solder_to(xor.input2)
rom.output_data.solder_to(prog_cnt_calc.mux.data1)
rom.output_address.solder_to(alu.mux.select0)
rom.output_address.solder_to(prog_cnt_calc.mux.select0)

# XOR to ALU
xor.output.solder_to(alu.mux.data0)

# ALU to Register
alu.mux.output.solder_to(register.data)

# Addres Pointer to ProgCounter
prog_cnt_calc.mux.output.solder_to(prog_cnt.data)


####################################
## Prepare execution
####################################

# Check that all inputs are connected
wiring_checker.check()

# Set the program code
rom.programming([
    DipSwitch(0, 0),  # XOR 0
    DipSwitch(0, 1),  # XOR 1
])

####################################
## Run the simulation
####################################
asyncio.run(clock.run())
