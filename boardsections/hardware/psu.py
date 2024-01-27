"""Simulate the Power Supply Unit

It has ground and Vcc wires. The Vcc is only on high voltage when the PSU is
switched on. All powered HW elements (like ICs) block their output wires, i.e.
they do not emit voltage change signals, when not powered.
"""

from collections.abc import Callable
import logging

from PySide6 import QtCore

from boardsections.hardware.wiring import Wire
from typedefinitions import TTL


class Psu:
    def __init__(self) -> None:
        self.ground = Ground()
        self.vcc = Vcc()
    
    @QtCore.Slot(bool)
    def power_switch(self, on: bool) -> None:
        """Switch the PSU on or off"""
        self.ground.output.set_output_level(TTL.L)
        self.vcc.output.set_output_level(TTL.H if on else TTL.L)
        logging.info(f"Board powered {'on' if on else 'off'}")


class Ground:
    """Fixed wiring to the ground
    
    When an input is soldered to the ground, it is automatically sent a signal
    with LOW.
    """
    def __init__(self) -> None:
        self.output = Wire("ground")

    def solder_to(self, input: Callable[[TTL], None]) -> None:
        """Solder ground to the input"""
        self.output.solder_to(input)
        logging.debug(f"Ground soldered to {input}")


class Vcc:
    """Voltage Common Collector
    
    When an input is soldered to the Vcc, it immediately sends a signal with
    LOW, then HIGH when the PSU is switched on and LOW when the PSU is switched
    off.
    """
    def __init__(self) -> None:
        self.output = Wire("Vcc")

    def solder_to(self, input: Callable[[TTL], None]) -> None:
        """Solder Vcc to the input"""
        self.output.solder_to(input)
        logging.debug(f"Vcc soldered to {input}")


PSU = Psu()
