from models.common.io import IOHandler
from .parser import parse_valve_graph
from .logic import maximum_pressure_release, Volcano


def aoc_2022_d16(io_handler: IOHandler) -> None:
    print("--- AOC 2022 - Day 16: Proboscidea Volcanium ---")
    graph = parse_valve_graph(
        io_handler.input_reader, time_to_travel_between_valves=1, time_to_open_valves=1
    )
    starting_valve = next(valve for valve in graph.nodes() if valve.valve_id == "AA")
    volcano = Volcano(graph, starting_valve, time_until_eruption=30)
    max_pressure_one_worker = maximum_pressure_release(volcano, num_workers=1)
    print(f"Part 1: Maximum pressure release is {max_pressure_one_worker}")
    volcano = Volcano(graph, starting_valve, time_until_eruption=26)
    print(
        "Part 2: Be patient, it takes about 1 minute to run",
        end="\r",
    )
    max_pressure_two_workers = maximum_pressure_release(
        volcano, num_workers=2, lower_bound=max_pressure_one_worker
    )
    print(
        f"Part 2: Maximum pressure release with elephant helper is {max_pressure_two_workers}"
    )
