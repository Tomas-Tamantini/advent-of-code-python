from typing import Iterator

from models.common.graphs import explore_with_bfs
from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D

from .lattice_graph import build_lattice_graph


def aoc_2018_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 20, "A Regular Map")
    io_handler.output_writer.write_header(problem_id)
    regex = io_handler.input_reader.read().strip()
    graph = build_lattice_graph(regex)
    starting_node = Vector2D(0, 0)
    distances = {
        node: distance for node, distance in explore_with_bfs(graph, starting_node)
    }
    result = max(distances.values())
    yield ProblemSolution(
        problem_id, f"Maximum distance from starting node: {result}", result, part=1
    )

    num_rooms_at_least_1000 = sum(d >= 1000 for d in distances.values())
    yield ProblemSolution(
        problem_id,
        f"Number of rooms at least 1000 doors away: {num_rooms_at_least_1000}",
        part=2,
        result=num_rooms_at_least_1000,
    )
