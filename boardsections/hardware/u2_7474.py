"""Simulate the 7474 dual flip-flop IC"""

import logging

from boardsections.hardware.wiring import Wire
from typedefinitions import TTL


PRESET_BIT_MASK = 0b10
CLEAR_BIT_MASK = 0b01


class FlipFlop:
    def __init__(self, output_q: Wire, output_q_inv: Wire) -> None:
        self.data_value: TTL = TTL.L
        self.state_bits: int = 1*PRESET_BIT_MASK + 1*CLEAR_BIT_MASK
        self.output_q = output_q
        self.output_q_inv = output_q_inv

    def data(self, new_value: TTL) -> None:
        """Slot: data changed"""
        self.data_value = new_value

    def clock(self, new_value: TTL) -> None:
        """Slot: clock changed"""
        # In normal mode, LOW->HIGH edge of clock changes output with data value
        if self.state_bits == 3 and new_value == TTL.H:
            self._output_changes()

    def preset_inv(self, new_value: TTL) -> None:
        """Slot: preset changed"""
        if self.state_bits&PRESET_BIT_MASK == new_value.value*PRESET_BIT_MASK:
            return
        # Flip the preset bit and keep the clear bit
        self.state_bits = new_value.value*PRESET_BIT_MASK + self.state_bits&CLEAR_BIT_MASK
        # Output changes if preset or clear is/are active now
        if self.state_bits:
            self._output_changes()

    def clear_inv(self, new_value: TTL) -> None:
        """Slot: clear changed"""
        if self.state_bits&CLEAR_BIT_MASK == new_value.value*CLEAR_BIT_MASK:
            return
        # Flip the clear bit and keep the preset bit
        self.state_bits = new_value.value*CLEAR_BIT_MASK + self.state_bits&PRESET_BIT_MASK
        # Output changes if preset or clear is/are active now
        if self.state_bits:
            self._output_changes()

    def _output_changes(self) -> None:
        """Output needs to change"""
        match self.state_bits:
            case 3:  # normal
                q = self.data_value
                q_inv = ~self.data_value
            case 2:  # clear
                q = TTL.L
                q_inv = TTL.H
            case 1:  # preset
                q = TTL.H
                q_inv = TTL.L
            case 0:  # invalid
                q = TTL.H
                q_inv = TTL.H
                logging.warning("Active PRE and CLR at the same time is invalid")
        self.output_q.changes_to(q)
        self.output_q_inv.changes_to(q_inv)
