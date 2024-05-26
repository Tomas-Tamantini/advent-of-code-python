from models.common.io import InputReader
from .parser import parse_valve_graph
from .logic import maximum_pressure_release


def aoc_2022_d16(input_reader: InputReader, **_) -> None:
    print("--- AOC 2022 - Day 16: Proboscidea Volcanium ---")
    graph = parse_valve_graph(input_reader, time_to_travel_between_valves=1)
    starting_valve = next(valve for valve in graph.nodes() if valve.valve_id == "AA")
    max_pressure = maximum_pressure_release(graph, starting_valve, total_time=30)
    print(f"Part 1: Maximum pressure release is {max_pressure}")
