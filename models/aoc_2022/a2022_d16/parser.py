from models.common.io import InputReader
from models.common.graphs import Maze
from .logic import Valve


def parse_valve_graph(
    input_reader: InputReader, time_to_travel_between_valves: int
) -> Maze:
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

    graph = Maze()
    for line in lines:
        current_valve_id = line.split()[1].strip()
        neighbors_str = line.replace("valves", "valve").split("valve")[-1].strip()
        for neighbor in neighbors_str.split(","):
            neighbor_id = neighbor.strip()
            graph.add_edge(
                valves[current_valve_id],
                valves[neighbor_id],
                time_to_travel_between_valves,
            )
    return graph
