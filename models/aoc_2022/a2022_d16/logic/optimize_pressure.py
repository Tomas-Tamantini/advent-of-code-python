from .volcano import Volcano
from .volcano_worker import VolcanoWorker, WorkerState
from .volcano_state import VolcanoState


def maximum_pressure_release(volcano: Volcano, num_workers: int) -> int:
    inital_state = VolcanoState(
        elapsed_time=0,
        pressure_released=0,
        open_valves=set(),
        workers=tuple(
            VolcanoWorker(state=WorkerState.IDLE, valve=volcano.starting_valve)
            for _ in range(num_workers)
        ),
    )
    explore_stack = [inital_state]
    maximum_pressure_release_so_far = 0
    while explore_stack:
        current_state = explore_stack.pop()
        # Branch and bound
        if (
            current_state.pressure_release_upper_bound(volcano)
            > maximum_pressure_release_so_far
        ):
            maximum_pressure_release_so_far = max(
                maximum_pressure_release_so_far, current_state.pressure_released
            )
            for next_state in current_state.next_states(volcano):
                explore_stack.append(next_state)
    return maximum_pressure_release_so_far
