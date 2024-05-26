from dataclasses import dataclass
from typing import Optional
from enum import Enum
from .valve import Valve


class WorkerState(Enum):
    IDLE = 1
    OPENING_VALVE = 2
    WAITING_FOR_ERUPTION = 3


@dataclass(frozen=True)
class VolcanoWorker:
    state: WorkerState
    valve: Valve
    task_completion_time: int = 0

    def go_idle(self) -> "VolcanoWorker":
        return VolcanoWorker(
            state=WorkerState.IDLE,
            valve=self.valve,
            task_completion_time=self.task_completion_time,
        )

    def wait_for_eruption(self, task_completion_time: int) -> "VolcanoWorker":
        return VolcanoWorker(
            state=WorkerState.WAITING_FOR_ERUPTION,
            valve=self.valve,
            task_completion_time=task_completion_time,
        )

    def start_opening_valve(
        self, task_completion_time: int, valve: Optional[Valve] = None
    ) -> "VolcanoWorker":
        valve = valve or self.valve
        return VolcanoWorker(WorkerState.OPENING_VALVE, valve, task_completion_time)
