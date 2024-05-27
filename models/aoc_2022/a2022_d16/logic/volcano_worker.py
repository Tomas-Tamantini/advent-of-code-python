from dataclasses import dataclass
from typing import Optional
from enum import Enum
from .valve import Valve


@dataclass(frozen=True)
class VolcanoWorker:
    is_idle: bool
    valve: Valve
    task_completion_time: int = 0

    def go_idle(self) -> "VolcanoWorker":
        return VolcanoWorker(
            is_idle=True,
            valve=self.valve,
            task_completion_time=self.task_completion_time,
        )

    def start_opening_valve(
        self, task_completion_time: int, valve: Optional[Valve] = None
    ) -> "VolcanoWorker":
        valve = valve or self.valve
        return VolcanoWorker(False, valve, task_completion_time)
