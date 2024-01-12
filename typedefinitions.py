"""Definitions"""

import dataclasses
from enum import Enum
from typing import Literal, Self


@dataclasses.dataclass
class Bit:
    value: Literal[0, 1]
    
    def ttl(self) -> "TTL":
        return TTL(self.value)


class TTL(Enum):
    L = 0
    H = 1

    def __and__(self, other: Self) -> Self:
        return self.__class__(self.value and other.value)
    
    def __or__(self, other: Self) -> Self:
        return self.__class__(self.value or other.value)

    def __invert__(self) -> Self:
        return self.__class__(not self.value)
    
    def voltage(self) -> float:
        return 0.3 + self.value*4.2

    def bit(self) -> Bit:
        return Bit(self.value)
