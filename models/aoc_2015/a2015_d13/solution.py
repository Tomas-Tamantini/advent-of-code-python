from models.common.io import IOHandler
from .parser import parse_seating_arrangement


def aoc_2015_d13(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2015 - Day 13: Knights of the Dinner Table ---")
    graph = parse_seating_arrangement(io_handler.input_reader)
    max_happiness = graph.both_ways_trip_max_cost()
    print(f"Part 1: Maximum happiness without me is {max_happiness}")
    pre_existing_nodes = list(graph.nodes())
    for n in pre_existing_nodes:
        graph.add_edge("Me", n, 0)
        graph.add_edge(n, "Me", 0)
    max_happiness = graph.both_ways_trip_max_cost()
    print(f"Part 2: Maximum happiness with me is {max_happiness}")
