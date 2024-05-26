from models.common.graphs import Maze
from ..logic import Volcano, Valve


def _build_valve(valve_id: chr = "A", flow_rate: int = -1, time_to_open: int = 1):
    if flow_rate < 0:
        flow_rate = ord(valve_id)
    return Valve(valve_id, flow_rate, time_to_open)


def test_volcano_collapses_valves_with_zero_flow_rate_and_just_two_neighbors():
    graph = Maze()
    a = _build_valve("A", flow_rate=0)
    b = _build_valve("B", flow_rate=0)
    c = _build_valve("C", flow_rate=1)
    graph.add_edge(a, b, weight=2)
    graph.add_edge(b, c, weight=7)
    volcano = Volcano(graph, starting_valve=a, time_until_eruption=30)
    assert set(volcano.all_valves()) == {a, c}
    assert set(volcano.neighboring_valves_with_travel_time(a)) == {(c, 9)}
    assert set(volcano.neighboring_valves_with_travel_time(c)) == {(a, 9)}


def test_volcano_keeps_track_of_minimum_travel_time():
    graph = Maze()
    graph.add_edge(_build_valve("A"), _build_valve("B"), weight=11)
    graph.add_edge(_build_valve("A"), _build_valve("D"), weight=7)
    graph.add_edge(_build_valve("B"), _build_valve("C"), weight=13)
    volcano = Volcano(graph, starting_valve=_build_valve("A"), time_until_eruption=30)
    assert volcano.min_travel_time == 7


def test_volcano_keeps_track_of_minimum_time_to_open_valve():
    graph = Maze()
    graph.add_edge(
        _build_valve("A", time_to_open=4), _build_valve("B", time_to_open=7), weight=1
    )
    graph.add_edge(
        _build_valve("B", time_to_open=7), _build_valve("C", time_to_open=3), weight=1
    )
    volcano = Volcano(
        graph, starting_valve=_build_valve("A", time_to_open=4), time_until_eruption=30
    )
    assert volcano.min_time_to_open_valve == 3
