"""Clock function"""

import asyncio
from collections.abc import Callable

from boardsections.hardware.leds import ClockLed
# from boardsections.hardware.u1_7414 import histerezis
from typedefinitions import TTL


class AstableMultivibrator:
    """Astable multivibrator creates the clock signal"""
    clock_level: TTL

    def __init__(self, clock_change_callback: Callable[[TTL], None]) -> None:
        self.clock_level = TTL.L
        self.clock_change_callback = clock_change_callback
        self.clock_led = ClockLed()

    async def run(self):
        while True:
            self.clock_change_callback(self.clock_level)
            await asyncio.sleep(1.0)
            self.clock_level = ~self.clock_level
            self.clock_led.set_voltage(self.clock_level.voltage())
