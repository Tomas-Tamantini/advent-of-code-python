from typing import Optional
from models.common.graphs import WeightedUndirectedGraph
from .valve import Valve
from .valves_state import ValvesState


def maximum_pressure_release(
    valves_graph: WeightedUndirectedGraph,
    starting_valve: Valve,
    total_time: int,
) -> int:
    _collapse_useless_valves(valves_graph, starting_valve)
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


def _next_valve_to_remove(
    valves_graph: WeightedUndirectedGraph, starting_valve: Valve
) -> Optional[Valve]:
    for valve in valves_graph.nodes():
        if (
            (valve != starting_valve)
            and (valve.flow_rate == 0)
            and (len(tuple(valves_graph.neighbors(valve))) <= 2)
        ):
            return valve


def _collapse_useless_valves(
    valves_graph: WeightedUndirectedGraph, starting_valve: Valve
) -> None:
    while (
        valve_to_remove := _next_valve_to_remove(valves_graph, starting_valve)
    ) is not None:
        neighbors = list(valves_graph.neighbors(valve_to_remove))
        if len(neighbors) == 2:
            previous_weight = valves_graph.weight(*neighbors)
            new_weight = sum(
                valves_graph.weight(valve_to_remove, neighbor) for neighbor in neighbors
            )
            valves_graph.add_edge(*neighbors, min(previous_weight, new_weight))
        valves_graph.remove_node(valve_to_remove)
