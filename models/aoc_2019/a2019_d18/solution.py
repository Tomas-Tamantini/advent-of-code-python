from models.common.io import InputReader
from .parser import parse_tunnel_maze


def aoc_2019_d18(input_reader: InputReader, **_) -> None:
    print("--- AOC 2019 - Day 18: Many-Worlds Interpretation ---")
    maze = parse_tunnel_maze(input_reader)
    min_dist = maze.shortest_distance_to_all_keys()
    print(f"Part 1: Minimum distance to collect all keys with one robot is {min_dist}")
    maze = parse_tunnel_maze(input_reader, split_entrance_four_ways=True)
    min_dist = maze.shortest_distance_to_all_keys()
    print(
        f"Part 2: Minimum distance to collect all keys with four robots is {min_dist}"
    )
