from dataclasses import dataclass
from enum import Enum


class PulseType(Enum):
    LOW = 0
    HIGH = 1


@dataclass(frozen=True)
class Pulse:
    origin: str
    destination: str
    pulse_type: PulseType
