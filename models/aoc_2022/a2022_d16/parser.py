from models.common.io import InputReader
from models.common.graphs import DirectedGraph
from .logic import Valve


def parse_valve_graph(input_reader: InputReader) -> DirectedGraph:
    lines = [
        l.replace(";", "").replace("rate=", "")
        for l in input_reader.read_stripped_lines()
    ]
    valves = dict()
    for line in lines:
        parts = line.split()
        valve_id = parts[1].strip()
        flow_rate = int(parts[4])
        valve = Valve(valve_id, flow_rate)
        valves[valve_id] = valve

    graph = DirectedGraph()
    for line in lines:
        current_valve_id = line.split()[1].strip()
        neighbors_str = line.replace("valves", "valve").split("valve")[-1].strip()
        for neighbor in neighbors_str.split(","):
            neighbor_id = neighbor.strip()
            graph.add_edge(valves[current_valve_id], valves[neighbor_id])
    return graph
