from models.common.io import IOHandler
from models.common.vectors import Vector2D
from models.common.graphs import explore_with_bfs
from .lattice_graph import build_lattice_graph


def aoc_2018_d20(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2018, 20, "A Regular Map")
    regex = io_handler.input_reader.read().strip()
    graph = build_lattice_graph(regex)
    starting_node = Vector2D(0, 0)
    distances = {
        node: distance for node, distance in explore_with_bfs(graph, starting_node)
    }
    max_distance = max(distances.values())
    print(f"Part 1: Maximum distance from starting node: {max_distance}")
    num_rooms_at_least_1000 = sum(d >= 1000 for d in distances.values())
    print(
        f"Part 2: Number of rooms at least 1000 doors away: {num_rooms_at_least_1000}"
    )
