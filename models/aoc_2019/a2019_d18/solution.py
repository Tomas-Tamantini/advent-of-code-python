from models.common.io import IOHandler
from .parser import parse_tunnel_maze


def aoc_2019_d18(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2019, 18, "Many-Worlds Interpretation")
    maze = parse_tunnel_maze(io_handler.input_reader)
    min_dist = maze.shortest_distance_to_all_keys()
    print(f"Part 1: Minimum distance to collect all keys with one robot is {min_dist}")
    maze = parse_tunnel_maze(io_handler.input_reader, split_entrance_four_ways=True)
    min_dist = maze.shortest_distance_to_all_keys()
    print(
        f"Part 2: Minimum distance to collect all keys with four robots is {min_dist}"
    )
