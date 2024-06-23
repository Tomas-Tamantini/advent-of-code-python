from models.common.io import IOHandler, Problem, ProblemSolution
from .polymer_reaction import polymer_reaction, minimum_polymer_length


def aoc_2018_d5(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 5, "Alchemical Reduction")
    io_handler.output_writer.write_header(problem_id)
    polymer = io_handler.input_reader.read().strip()
    reacted_polymer = polymer_reaction(polymer)
    solution = ProblemSolution(
        problem_id, f"Length of reacted polymer: {len(reacted_polymer)}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    min_length = minimum_polymer_length(polymer)
    solution = ProblemSolution(
        problem_id, f"Minimum length of polymer: {min_length}", part=2
    )
    io_handler.output_writer.write_solution(solution)
