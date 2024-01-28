"""Definitions"""

from enum import Enum
import math
from typing import Literal, Self


# @dataclasses.dataclass
# class Bit:
#     value: Literal[0, 1]
    
#     def ttl(self) -> "TTL":
#         return TTL(self.value)


class TTL(Enum):
    L = 0
    H = 1

    def __and__(self, other: Self) -> Self:
        return self.__class__(self.value and other.value)
    
    def __or__(self, other: Self) -> Self:
        return self.__class__(self.value or other.value)

    def __invert__(self) -> Self:
        return self.__class__(not self.value)
    
    def to_volt(self) -> "Voltage":
        return Voltage(0.3 + self.value*4.2)

    # def bit(self) -> Bit:
    #     return Bit(self.value)


class Voltage:
    # The max diff between voltage values when we consider them the same
    VOLTAGE_TOLERANCE = 0.1

    def __init__(self, level: Self | float | int) -> None:
        self.level: float = self._get_level(level)

    def _get_level(self, other: Self | float | int) -> float:
        if isinstance(other, self.__class__):
            return other.level
        return float(other)
    
    def __add__(self, other: Self | float | int) -> Self:
        return self.__class__(self.level + self._get_level(other))

    def __sub__(self, other: Self | float | int) -> Self:
        return self.__class__(self.level - self._get_level(other))
    
    def __mul__(self, other: Self | float | int) -> Self:
        return self.__class__(self.level * self._get_level(other))
    
    def __truediv__(self, other: Self | float | int) -> Self:
        return self.__class__(self.level / self._get_level(other))
    
    def __gt__(self, other: Self | float | int) -> bool:
        return self.level > self._get_level(other)
    
    def __lt__(self, other: Self | float | int) -> bool:
        return self.level < self._get_level(other)
    
    def __eq__(self, other: Self | float | int) -> bool:
        return math.isclose(
                self.level,
                self._get_level(other),
                abs_tol=self.VOLTAGE_TOLERANCE
            )
    
    def __eq__(self, other: Self | float | int) -> bool:
        return not self.__eq__(other)

    def to_ttl(self) -> TTL:
        return TTL(1 if self.level>2.5 else 0)
