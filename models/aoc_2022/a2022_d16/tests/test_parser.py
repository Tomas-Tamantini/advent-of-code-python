from models.common.io import InputFromString
from ..parser import parse_valve_graph
from ..logic import Valve


def test_parse_valve_graph():
    input_reader = InputFromString(
        """
        Valve AA has flow rate=22; tunnels lead to valves BB, CC
        Valve BB has flow rate=13; tunnels lead to valve AA
        Valve CC has flow rate=15; tunnels lead to valve AA
        """
    )
    graph = parse_valve_graph(input_reader, time_to_travel_between_valves=123)
    valve_a = Valve("AA", 22)
    valve_b = Valve("BB", 13)
    valve_c = Valve("CC", 15)
    assert set(graph.nodes()) == {valve_a, valve_b, valve_c}
    assert set(graph.neighbors(valve_a)) == {valve_b, valve_c}
    assert set(graph.neighbors(valve_b)) == {valve_a}
    assert set(graph.neighbors(valve_c)) == {valve_a}
    assert graph.weight(valve_a, valve_b) == 123
