from models.common.graphs import Maze
from .valve import Valve
from .valves_state import ValvesState


def maximum_pressure_release(
    valves_graph: Maze,
    starting_valve: Valve,
    total_time: int,
) -> int:
    valves_graph.reduce(
        irreducible_nodes={
            v for v in valves_graph.nodes() if (v.flow_rate > 0 or v == starting_valve)
        }
    )
    inital_state = ValvesState(
        current_valve=starting_valve,
        open_valves=set(),
        time_elapsed=0,
        pressure_released=0,
    )
    all_valves = set(valves_graph.nodes())
    explore_stack = [inital_state]
    maximum_pressure_release_so_far = 0
    while explore_stack:
        current_state = explore_stack.pop()
        # Branch and bound
        min_travel_time = min(
            valves_graph.weight(current_state.current_valve, neighbor)
            for neighbor in valves_graph.neighbors(current_state.current_valve)
        )
        if (
            current_state.pressure_release_upper_bound(
                total_time, min_travel_time, all_valves
            )
            > maximum_pressure_release_so_far
        ):
            maximum_pressure_release_so_far = max(
                maximum_pressure_release_so_far, current_state.pressure_released
            )
            for next_state in current_state.next_states(total_time, valves_graph):
                explore_stack.append(next_state)
    return maximum_pressure_release_so_far
