from typing import Iterator, Optional, Hashable
from .valve import Valve
from .volcano import Volcano
from .volcano_worker import VolcanoWorker, WorkerState


class VolcanoState:
    def __init__(
        self,
        elapsed_time: int,
        pressure_released: int,
        open_valves: set[Valve],
        workers: tuple[VolcanoWorker, ...],
    ) -> None:
        self._elapsed_time = elapsed_time
        self._pressure_released = pressure_released
        self._open_valves = open_valves
        self._workers = workers

    @property
    def elapsed_time(self) -> int:
        return self._elapsed_time

    @property
    def pressure_released(self) -> int:
        return self._pressure_released

    @property
    def workers(self) -> tuple[VolcanoWorker, ...]:
        return self._workers

    def _valve_is_being_opened(self, valve: Valve) -> bool:
        return valve in self._open_valves and any(
            (worker.state == WorkerState.OPENING_VALVE and worker.valve == valve)
            for worker in self._workers
        )

    def _index_of_idle_worker(self) -> Optional[int]:
        for i, worker in enumerate(self._workers):
            if worker.state == WorkerState.IDLE:
                return i

    def _can_open_valve_in_time(self, valve: Valve, time_until_eruption: int) -> bool:
        return (
            valve.flow_rate > 0
            and valve not in self._open_valves
            and not self._valve_is_being_opened(valve)
            and valve.time_to_open + self._elapsed_time < time_until_eruption
        )

    def _update_worker(
        self, worker_index: int, new_worker: VolcanoWorker
    ) -> "VolcanoState":
        new_workers = list(self._workers)
        new_workers[worker_index] = new_worker
        return VolcanoState(
            elapsed_time=self._elapsed_time,
            pressure_released=self._pressure_released,
            open_valves=self._open_valves,
            workers=tuple(new_workers),
        )

    def _start_opening_valve(self, worker_index: int) -> "VolcanoState":
        worker = self._workers[worker_index]
        new_worker = worker.start_opening_valve(
            task_completion_time=self._elapsed_time + worker.valve.time_to_open
        )
        return self._update_worker(worker_index, new_worker)

    def _travel_to_neighboring_valves(
        self, worker_index: int, volcano: Volcano
    ) -> Iterator["VolcanoState"]:
        worker = self._workers[worker_index]
        for valve in volcano.all_valves():
            if valve != worker.valve:
                travel_time = volcano.distance(worker.valve, valve)
                if self._can_open_valve_in_time(
                    valve, volcano.time_until_eruption - travel_time
                ):
                    new_worker = worker.start_opening_valve(
                        self._elapsed_time + travel_time + valve.time_to_open, valve
                    )
                    yield self._update_worker(worker_index, new_worker)

    def _wait_for_eruption(self, worker_index: int, volcano: Volcano) -> "VolcanoState":
        worker = self._workers[worker_index]
        new_worker = worker.wait_for_eruption(
            task_completion_time=volcano.time_until_eruption
        )
        return self._update_worker(worker_index, new_worker)

    def _put_to_work(
        self, idle_worker_index: int, volcano: Volcano
    ) -> Iterator["VolcanoState"]:
        no_jobs_can_be_completed_before_eruption = True
        worker = self._workers[idle_worker_index]
        if self._can_open_valve_in_time(worker.valve, volcano.time_until_eruption):
            no_jobs_can_be_completed_before_eruption = False
            yield self._start_opening_valve(idle_worker_index)
        for next_state in self._travel_to_neighboring_valves(
            idle_worker_index, volcano
        ):
            no_jobs_can_be_completed_before_eruption = False
            yield next_state
        if no_jobs_can_be_completed_before_eruption:
            yield self._wait_for_eruption(idle_worker_index, volcano)

    def _finish_task(self, worker_index: int) -> "VolcanoState":
        worker = self._workers[worker_index]
        time_interval = worker.task_completion_time - self._elapsed_time
        pressure_increment = sum(o.flow_rate * time_interval for o in self._open_valves)
        new_worker = worker.go_idle()
        new_workers = list(self._workers)
        new_workers[worker_index] = new_worker
        if worker.state == WorkerState.OPENING_VALVE:
            new_open_valves = self._open_valves | {worker.valve}
        else:
            new_open_valves = self._open_valves
        return VolcanoState(
            elapsed_time=self.elapsed_time + time_interval,
            pressure_released=self.pressure_released + pressure_increment,
            open_valves=new_open_valves,
            workers=tuple(new_workers),
        )

    def _index_of_next_worker_to_finish_task(self) -> int:
        min_time = float("inf")
        next_index = None
        for i, worker in enumerate(self._workers):
            if not worker.state == WorkerState.IDLE:
                if worker.task_completion_time <= min_time:
                    min_time = worker.task_completion_time
                    next_index = i
        if next_index is None:
            raise NotImplementedError()
        return next_index

    def next_states(self, volcano: Volcano) -> Iterator["VolcanoState"]:
        if self._elapsed_time >= volcano.time_until_eruption:
            return
        elif (idle_worker_index := self._index_of_idle_worker()) is not None:
            yield from self._put_to_work(idle_worker_index, volcano)
        else:
            index_of_worker_to_finish = self._index_of_next_worker_to_finish_task()
            next_worker_to_finish = self._workers[index_of_worker_to_finish]
            if (
                next_worker_to_finish.task_completion_time
                <= volcano.time_until_eruption
            ):
                yield self._finish_task(index_of_worker_to_finish)
            else:
                raise NotImplementedError()

    def pressure_release_upper_bound(self, volcano: Volcano) -> int:
        upper_bound = self._pressure_released
        extended_open_valves = self._open_valves | {w.valve for w in self._workers}
        remaining_valves = set(volcano.all_valves()) - extended_open_valves
        sorted_remaning = list(sorted(remaining_valves, key=lambda v: -v.flow_rate))
        if (time_remaining := volcano.time_until_eruption - self._elapsed_time) > 0:
            upper_bound += sum(
                v.flow_rate * time_remaining for v in extended_open_valves
            )
            step_size = len(self._workers)
            for worker_index in range(len(self._workers)):
                worker_remaining_time = time_remaining
                for idx_next_valve_to_open in range(
                    worker_index, len(sorted_remaning), step_size
                ):
                    worker_remaining_time -= (
                        volcano.min_travel_time + volcano.min_time_to_open_valve
                    )
                    if worker_remaining_time <= 0:
                        break
                    next_valve_to_open = sorted_remaning[idx_next_valve_to_open]
                    upper_bound += worker_remaining_time * next_valve_to_open.flow_rate
        return upper_bound

    def _as_hashable(self) -> Hashable:
        return (
            self._elapsed_time,
            self._pressure_released,
            frozenset(self._open_valves),
            frozenset(self._workers),
        )

    def __eq__(self, value: object) -> bool:
        return self._as_hashable() == value._as_hashable()

    def __hash__(self) -> int:
        return hash(self._as_hashable())
