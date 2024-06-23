from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_program_tree


def aoc_2017_d7(io_handler: IOHandler) -> None:
    problem_id = Problem(2017, 7, "Recursive Circus")
    io_handler.output_writer.write_header(problem_id)
    root = parse_program_tree(io_handler.input_reader)
    solution = ProblemSolution(problem_id, f"Root node: {root.name}", part=1)
    io_handler.output_writer.write_solution(solution)
    imbalance = root.weight_imbalance()
    solution = ProblemSolution(
        problem_id, f"Weight to fix imbalance: {imbalance.expected_weight}", part=2
    )
    io_handler.output_writer.write_solution(solution)
