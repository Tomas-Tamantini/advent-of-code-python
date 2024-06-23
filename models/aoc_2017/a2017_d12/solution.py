from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_program_graph


def aoc_2017_d12(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 12, "Digital Plumber")
    io_handler.output_writer.write_header(problem_id)
    program_graph = parse_program_graph(io_handler.input_reader)
    disjoint_groups = list(program_graph.disjoint_groups())
    initial_node = 0
    group_size = -1
    for group in disjoint_groups:
        if initial_node in group:
            group_size = len(group)
            break
    solution = ProblemSolution(
        problem_id,
        f"Number of nodes in group with node {initial_node}: {group_size}",
        part=1,
    )
    io_handler.set_solution(solution)
    solution = ProblemSolution(
        problem_id, f"Number of disjoint groups: {len(disjoint_groups)}", part=2
    )
    io_handler.set_solution(solution)
