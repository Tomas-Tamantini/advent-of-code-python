from dataclasses import dataclass
from enum import Enum
from queue import PriorityQueue

from models.common.graphs import DirectedGraph


class _Event(Enum):
    JOB_FREE = "job free"
    JOB_DONE = "job done"


@dataclass
class _State:
    num_idle_workers: int
    free_jobs: set[str]
    jobs_accounted_for: set[str]

    def pop_next_free_job(self) -> str:
        next_job = min(self.free_jobs)
        self.free_jobs.remove(next_job)
        return next_job


def _add_free_jobs_to_event_queue(
    time: int,
    jobs_dag: DirectedGraph,
    state: _State,
    event_queue: PriorityQueue,
) -> None:
    for job in jobs_dag.nodes():
        if job not in state.jobs_accounted_for and not set(jobs_dag.incoming(job)):
            event_queue.put((time, job, _Event.JOB_FREE))
            state.jobs_accounted_for.add(job)


def _take_next_free_job(job_durations, state, time, event_queue) -> None:
    next_job = state.pop_next_free_job()
    event_queue.put((time + job_durations[next_job], next_job, _Event.JOB_DONE))
    state.num_idle_workers -= 1


def time_to_complete_jobs(
    num_workers: int,
    jobs_dag: DirectedGraph,
    job_durations: dict[str, int],
) -> int:
    state = _State(
        num_idle_workers=num_workers,
        free_jobs=set(),
        jobs_accounted_for=set(),
    )
    time = 0
    event_queue = PriorityQueue()
    _add_free_jobs_to_event_queue(time, jobs_dag, state, event_queue)
    while not event_queue.empty():
        time, job, event = event_queue.get()
        if event == _Event.JOB_FREE:
            state.free_jobs.add(job)
            if state.num_idle_workers > 0:
                _take_next_free_job(job_durations, state, time, event_queue)
        elif event == _Event.JOB_DONE:
            state.num_idle_workers += 1
            jobs_dag.remove_node(job)
            _add_free_jobs_to_event_queue(time, jobs_dag, state, event_queue)
            if state.free_jobs:
                _take_next_free_job(job_durations, state, time, event_queue)
    return time
