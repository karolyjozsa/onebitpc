"""Simulate the LEDs"""

from PySide6 import QtCore

from tools.wiring_checker import hw_elem, input
from typedefinitions import TTL, Voltage


# The voltage on the LED when it is considered ON
LIGHTUP_VOLTAGE = Voltage(4.1)


@hw_elem
class Led:
    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
        self.catode_level: Voltage = Voltage(0.0)
        self.anode_level: Voltage = Voltage(0.0)
        self.is_on = False

    @input
    @QtCore.Slot(TTL)
    def anode(self, new_value: TTL | Voltage) -> None:
        self._changed("anode_level", new_value)

    @input
    @QtCore.Slot(TTL)
    def catode(self, new_value: TTL | Voltage) -> None:
        self._changed("catode_level", new_value)

    def _changed(self, side: str, new_value: TTL | Voltage):
        if isinstance(new_value, TTL):
            new_volt_value = new_value.to_volt()
        else:
            new_volt_value = new_value
        setattr(self, side, new_volt_value)
        self.is_on = (self.anode_level - self.catode_level) > LIGHTUP_VOLTAGE
        print(f'{self.name} LED {"ON" if self.is_on else "OFF"}')
