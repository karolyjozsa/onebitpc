"""Connect the board sections

It is the board soldering. The connected items can be HW elements or logical
blocks:

- ROM
- Clock
- CPU register (memory)
- CPU program counter storage
- An arithmetic processor (a multiplexer) setting the Register
- A program counter calculator (a multiplexer) setting the ProgCounter
- LEDs
- Reset button
"""

from boardsections.clock import AstableMultivibrator
from boardsections.cpu import Alu, AddrPtr, Xor
from boardsections.hardware.dipswitches import DipSwitch
from boardsections.hardware.leds import ClockLed, ProgCountLed, RegisterLed
from boardsections.hardware.u2_7474 import FlipFlop
from boardsections.hardware.wiring import Wire
from boardsections.rom import Rom


class Board:
    def __init__(self) -> None:
        # Reset button
        # ??????

        # LEDs
        self.register_led = RegisterLed()
        self.pc_led = ProgCountLed()
        self.clock_led = ClockLed()

        # Complex sections
        self.clock = AstableMultivibrator(Wire())
        self.rom = Rom(Wire())
        self.register = FlipFlop(Wire(), Wire())
        self.prog_cnt = FlipFlop(Wire(), Wire())

        # Create calculating sections
        self.xor = Xor(Wire())
        self.alu = Alu()
        self.addr_ptr = AddrPtr()


        # Solder the clock output to Register, ProgCounter and LED
        self.clock.output.solder_to(self.register.clock)
        self.clock.output.solder_to(self.prog_cnt.clock)
        self.clock.output.solder_to(self.clock_led.anode)

        # Solder the Register output to XOR, ALU and LED
        self.register.output_q.solder_to(self.xor.input1)
        self.register.output_q.solder_to(self.alu.mux.data1)
        self.register.output_q.solder_to(self.register_led.anode)

        # Solder the Program Counter output to ROM, Addres Pointer and LED
        self.prog_cnt.output_q.solder_to(self.rom.address)
        self.prog_cnt.output_q_inv.solder_to(self.addr_ptr.mux.data0)
        self.prog_cnt.output_q.solder_to(self.pc_led.anode)

        # Solder the ROM output to arithmetic and addressing sections
        self.rom.output_data.solder_to(self.xor.input2)
        self.rom.output_data.solder_to(self.addr_ptr.mux.data1)
        self.rom.output_address.solder_to(self.alu.mux.select0)
        self.rom.output_address.solder_to(self.addr_ptr.mux.select0)

        # Solder the XOR output to ALU
        self.xor.output.solder_to(self.alu.mux.data0)

        # Solder the ALU output to Register
        self.alu.mux.output.solder_to(self.register.data)

        # Solder the Addres Pointer output to ProgCounter
        self.addr_ptr.mux.output.solder_to(self.prog_cnt.data)
