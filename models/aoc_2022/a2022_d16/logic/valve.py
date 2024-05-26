from typing import Hashable
from dataclasses import dataclass


@dataclass(frozen=True)
class Valve:
    valve_id: Hashable
    flow_rate: int
