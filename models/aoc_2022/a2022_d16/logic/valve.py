from dataclasses import dataclass
from typing import Hashable


@dataclass(frozen=True)
class Valve:
    valve_id: Hashable
    flow_rate: int
    time_to_open: int
