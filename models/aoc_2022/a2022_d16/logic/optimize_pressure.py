from models.common.graphs import Maze
from .valve import Valve
from .volcano import Volcano
from .valves_state import ValvesState


def maximum_pressure_release(
    valves_graph: Maze,
    starting_valve: Valve,
    total_time: int,
) -> int:
    volcano = Volcano(valves_graph, starting_valve)
    inital_state = ValvesState(
        current_valve=starting_valve,
        open_valves=set(),
        time_elapsed=0,
        pressure_released=0,
    )
    explore_stack = [inital_state]
    maximum_pressure_release_so_far = 0
    while explore_stack:
        current_state = explore_stack.pop()
        # Branch and bound
        if (
            current_state.pressure_release_upper_bound(total_time, volcano)
            > maximum_pressure_release_so_far
        ):
            maximum_pressure_release_so_far = max(
                maximum_pressure_release_so_far, current_state.pressure_released
            )
            for next_state in current_state.next_states(total_time, volcano):
                explore_stack.append(next_state)
    return maximum_pressure_release_so_far
