"""??"""

import dataclasses
from typing import Literal

@dataclasses.dataclass
class DipSwitch:
    switch_one: Literal[0, 1]
    switch_two: Literal[0, 1]

# There are 2x double-switches
dip_switch_array = [
    DipSwitch(0, 0),  # at address 0
    DipSwitch(0, 0),  # at address 1
]
