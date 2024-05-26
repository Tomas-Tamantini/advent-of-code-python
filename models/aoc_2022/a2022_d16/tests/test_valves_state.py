from models.common.graphs import Maze
from ..logic import Valve, ValvesState


def _example_valves() -> dict[chr, Valve]:
    flow_rates = {
        "A": 10,
        "B": 3,
        "C": 32,
        "D": 15,
        "E": 20,
        "F": 17,
        "G": 8,
        "H": 12,
        "I": 0,
    }
    return {
        valve_id: Valve(valve_id, flow_rate)
        for valve_id, flow_rate in flow_rates.items()
    }


def _example_state(current_valve_id: chr = "A", time_elapsed: int = 25):
    valves = _example_valves()
    return ValvesState(
        current_valve=valves[current_valve_id],
        open_valves={valves["B"], valves["C"]},
        time_elapsed=time_elapsed,
        pressure_released=13,
    )


def test_valves_state_has_no_next_state_if_time_is_up():
    time_elapsed = 25
    state = _example_state(time_elapsed=time_elapsed)
    valves = _example_valves()
    graph = Maze()
    graph.add_edge(valves["A"], valves["B"], weight=1)
    assert list(state.next_states(total_time=time_elapsed, valves_graph=graph)) == []


def test_valves_state_has_no_next_state_if_current_valve_is_open_and_has_no_neighbors():
    state = _example_state(current_valve_id="B")
    graph = Maze()
    assert list(state.next_states(total_time=30, valves_graph=graph)) == []


def test_valves_state_can_open_current_valve_if_not_open_yet():
    state = _example_state(current_valve_id="A")
    valves = _example_valves()
    graph = Maze()
    next_states = list(state.next_states(total_time=30, valves_graph=graph))
    assert len(next_states) == 1
    next_state = next_states[0]
    assert next_state.current_valve == valves["A"]
    assert next_state.open_valves == {valves[c] for c in "ABC"}
    assert next_state.time_elapsed == 26
    assert next_state.pressure_released == 48


def test_valves_state_cannot_open_current_valve_if_its_flow_rate_is_zero():
    state = _example_state(current_valve_id="I")
    graph = Maze()
    assert list(state.next_states(total_time=30, valves_graph=graph)) == []


def test_valves_state_can_go_to_neighboring_valve_if_reachable():
    state = _example_state(current_valve_id="B")
    valves = _example_valves()
    graph = Maze()
    graph.add_edge(valves["B"], valves["H"], weight=3)
    next_states = list(state.next_states(total_time=30, valves_graph=graph))
    assert len(next_states) == 1
    next_state = next_states[0]
    assert next_state.current_valve == valves["H"]
    assert next_state.open_valves == {valves[c] for c in "BC"}
    assert next_state.time_elapsed == 28
    assert next_state.pressure_released == 118


def test_pressure_release_upper_bound_uses_minimum_time_to_travel_between_valves_and_open_them():
    state = _example_state()
    assert (
        state.pressure_release_upper_bound(
            total_time=30, min_travel_time=1, all_valves=set(_example_valves().values())
        )
        == 315
    )
