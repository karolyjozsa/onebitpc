"""Simulate the 7414 6x Schmidt-Trigger IC"""

from boardsections.hardware.wiring import Wire
from typedefinitions import TTL


THRESHOLD_HIGH = 4.2
THRESHOLD_LOW = 0.6


class SchmidtTrigger:
    def __init__(self, output: Wire) -> None:
        self.output_value: TTL = TTL.L
        self.output = output
    
    def input(self, new_value: float | TTL) -> None:
        """Slot: input changed"""
        if isinstance(new_value, TTL):
            if new_value != self.output_value:
                self.output.changes_to(new_value)
            return

        if new_value > THRESHOLD_HIGH and self.output_value == TTL.L:
            self.output_value = TTL.H
            self.output.changes_to(self.output_value)

        if new_value < THRESHOLD_LOW and self.output_value == TTL.H:
            self.output_value = TTL.L
            self.output.changes_to(self.output_value)
