from dataclasses import dataclass
from enum import Enum
from .valve import Valve


class WorkerState(Enum):
    IDLE = 1
    OPENING_VALVE = 2
    EN_ROUTE = 3
    WAITING_FOR_ERUPTION = 4


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

    def start_opening_valve(self, task_completion_time: int) -> "VolcanoWorker":
        return VolcanoWorker(
            state=WorkerState.OPENING_VALVE,
            valve=self.valve,
            task_completion_time=task_completion_time,
        )

    def start_moving_towards(
        self, new_valve: Valve, task_completion_time: int
    ) -> "VolcanoWorker":
        return VolcanoWorker(
            state=WorkerState.EN_ROUTE,
            valve=new_valve,
            task_completion_time=task_completion_time,
        )
