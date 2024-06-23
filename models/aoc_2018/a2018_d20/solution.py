from models.common.io import IOHandler, Problem, ProblemSolution
from models.common.vectors import Vector2D
from models.common.graphs import explore_with_bfs
from .lattice_graph import build_lattice_graph


def aoc_2018_d20(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 20, "A Regular Map")
    io_handler.output_writer.write_header(problem_id)
    regex = io_handler.input_reader.read().strip()
    graph = build_lattice_graph(regex)
    starting_node = Vector2D(0, 0)
    distances = {
        node: distance for node, distance in explore_with_bfs(graph, starting_node)
    }
    max_distance = max(distances.values())
    solution = ProblemSolution(
        problem_id, f"Maximum distance from starting node: {max_distance}", part=1
    )
    io_handler.set_solution(solution)
    num_rooms_at_least_1000 = sum(d >= 1000 for d in distances.values())
    solution = ProblemSolution(
        problem_id,
        f"Number of rooms at least 1000 doors away: {num_rooms_at_least_1000}",
        part=2,
    )
    io_handler.set_solution(solution)
