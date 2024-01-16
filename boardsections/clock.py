"""Clock section on the board

- An astable multivibrator
"""

import asyncio

# from boardsections.hardware.u1_7414 import SchmidtTrigger
from boardsections.hardware.wiring import Wire
from typedefinitions import TTL


class AstableMultivibrator:
    """Astable multivibrator creates the clock pulses"""
    def __init__(self) -> None:
        self.clock_level = TTL.L
        self.output = Wire("astabilmv_out")

    async def run(self):
        while True:
            self.output.set_output_level(self.clock_level)
            await asyncio.sleep(1.0)
            self.clock_level = ~self.clock_level
            # TODO: use analogue simulation with SchmidtTrigger gates
