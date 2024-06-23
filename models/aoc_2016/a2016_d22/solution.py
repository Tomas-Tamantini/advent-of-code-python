from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_storage_nodes


def aoc_2016_d22(io_handler: IOHandler) -> None:
    problem_id = Problem(2016, 22, "Grid Computing")
    io_handler.output_writer.write_header(problem_id)
    nodes = list(parse_storage_nodes(io_handler.input_reader))
    viable_pairs = sum(
        node_a.makes_viable_pair(node_b) for node_a in nodes for node_b in nodes
    )
    solution = ProblemSolution(
        problem_id, f"Number of viable pairs: {viable_pairs}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    solution = ProblemSolution(
        problem_id, "Done by hand (move hole around grid)", part=2
    )
    io_handler.output_writer.write_solution(solution)
