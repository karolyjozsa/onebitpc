"""Power Supply Unit simulation

It has ground and Vcc wires. The Vcc is only on high voltage when the PSU is
switched on. All powered HW elements (like ICs) block their output wires, i.e.
they do not emit voltage change signals, when not powered.
"""

from collections.abc import Callable

from PySide6 import QtCore

from boardsections.hardware.wiring import Wire
from typedefinitions import TTL


class FixedWire:
    """Special HW element, i.e. fix wiring to ground or Vcc"""
    def __init__(self, name: str) -> None:
        self.output = Wire(name)


class Ground(FixedWire):
    """Fixed wiring to the ground
    
    When an input is soldered to the ground, it is automatically sent a signal
    with LOW.
    """
    def __init__(self) -> None:
        super().__init__("ground")

    def solder_to(self, input: Callable[[TTL], None]) -> None:
        """This replaces the original solder_to() to also sends signal"""
        self.output.solder_to(input)
        self.output.set_output_level(TTL.L)


class Vcc(FixedWire):
    """Voltage Common Collector
    
    When an input is soldered to the Vcc, it sends a signal with LOW
    immediately, then HIGH when the PSU is switched on and LOW when the PSU is
    switched off.
    """
    def __init__(self) -> None:
        super().__init__("Vcc")

    def solder_to(self, input: Callable[[TTL], None]) -> None:
        """This replaces the original solder_to() to also sends signal"""
        self.output.solder_to(input)
        self.power_switch(on=True)
    
    @QtCore.Slot(bool)
    def power_switch(self, on: bool) -> None:
        self.output.set_output_level(TTL.H if on else TTL.L)
