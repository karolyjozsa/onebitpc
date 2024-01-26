"""Simulate the 7474 dual flip-flop IC"""

import logging

from PySide6 import QtCore

from boardsections.hardware.psu import Vcc
from boardsections.hardware.wiring import Wire
from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL


PRESET_BIT_MASK = 0b10
CLEAR_BIT_MASK = 0b01


@hw_elem
class FlipFlop:
    def __init__(self, name: str) -> None:
        self.powered = False
        Vcc().solder_to(self.vcc)
        self.data_value: TTL = TTL.L
        self.state_bits: int = 0  # actually undefined, but PRE/CLR=High is coming
        self.output_q = Wire(f"{name}_q")
        self.output_q_inv = Wire(f"{name}_q_inv")

    @input
    @QtCore.Slot(TTL)
    def vcc(self, power: TTL) -> None:
        self.powered = power == TTL.H

    @input
    @QtCore.Slot(TTL)
    def data(self, new_value: TTL) -> None:
        self.data_value = new_value

    @input
    @QtCore.Slot(TTL)
    def clock(self, new_value: TTL) -> None:
        # In normal mode, LOW->HIGH edge of clock changes output with data value
        if self.state_bits == 3 and new_value == TTL.H:
            self._output_changes()

    @input
    @QtCore.Slot(TTL)
    def preset_inv(self, new_value: TTL) -> None:
        if self.state_bits&PRESET_BIT_MASK == new_value.value*PRESET_BIT_MASK:
            return
        # Flip the preset bit and keep the clear bit
        self.state_bits = new_value.value*PRESET_BIT_MASK + self.state_bits&CLEAR_BIT_MASK
        # Output changes if preset or clear is/are active now
        if self.state_bits:
            self._output_changes()

    @input
    @QtCore.Slot(TTL)
    def clear_inv(self, new_value: TTL) -> None:
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
        if self.powered:
            self.output_q.set_output_level(q)
            self.output_q_inv.set_output_level(q_inv)
