from models.common.graphs import WeightedUndirectedGraph
from ..logic import maximum_pressure_release, Valve


def test_optimizing_pressure_finds_maximum_pressure_release_in_given_time():
    flow_rates = {
        "AA": 0,
        "BB": 13,
        "CC": 2,
        "DD": 20,
        "EE": 3,
        "FF": 0,
        "GG": 0,
        "HH": 22,
        "II": 0,
        "JJ": 21,
    }
    connections = {
        "AA": {"DD", "II", "BB"},
        "BB": {"CC", "AA"},
        "CC": {"DD", "BB"},
        "DD": {"CC", "AA", "EE"},
        "EE": {"FF", "DD"},
        "FF": {"EE", "GG"},
        "GG": {"FF", "HH"},
        "HH": {"GG"},
        "II": {"AA", "JJ"},
        "JJ": {"II"},
    }
    valves = {
        valve_id: Valve(valve_id, flow_rate)
        for valve_id, flow_rate in flow_rates.items()
    }
    valves_graph = WeightedUndirectedGraph()
    for source, destinations in connections.items():
        for destination in destinations:
            valves_graph.add_edge(valves[source], valves[destination], weight=1)
    starting_valve = valves["AA"]
    assert maximum_pressure_release(valves_graph, starting_valve, total_time=30) == 1651
