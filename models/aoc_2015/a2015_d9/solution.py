from models.common.io import InputReader
from .parser import parse_undirected_graph


def aoc_2015_d9(input_reader: InputReader, **_) -> None:
    print("--- AOC 2015 - Day 9: All in a Single Night ---")
    graph = parse_undirected_graph(input_reader)
    shortest_distance = graph.shortest_complete_itinerary_distance()
    print(f"Part 1: Distance of shortest itinerary is {shortest_distance}")
    longest_distance = graph.longest_complete_itinerary_distance()
    print(f"Part 2: Distance of longest itinerary is {longest_distance}")
