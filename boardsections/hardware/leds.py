"""Simulate the LEDs"""

class Led:
    def __init__(self, name: str, color: str) -> None:
        self.name = name
        self.color = color
        self.voltage: float = 0.2

    def display(self) -> None:
        print(f'{self.name} LED is {"ON" if self.voltage > 4.2 else "OFF"}')

    def set_voltage(self, voltage: float) -> None:
        self.voltage = voltage
        self.display()

class RegisterLed(Led):
    def __init__(self) -> None:
        super().__init__('Reg', 'red')

class ProgCountLed(Led):
    def __init__(self) -> None:
        super().__init__('PC', 'yellow')

class ClockLed(Led):
    def __init__(self) -> None:
        super().__init__('Clock', 'blue')
