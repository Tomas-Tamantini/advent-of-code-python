from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_polymer_and_polymer_extension_rules
from .polymer_extension import PolymerExtension


def aoc_2021_d14(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 14, "Extended Polymerization")
    io_handler.output_writer.write_header(problem_id)
    polymer, rules = parse_polymer_and_polymer_extension_rules(io_handler.input_reader)
    extension = PolymerExtension(rules)
    character_count = extension.character_count_after_multiple_extensions(
        polymer, num_times=10
    )
    difference = max(character_count.values()) - min(character_count.values())
    solution = ProblemSolution(
        problem_id,
        f"The difference between the most and least common characters after 10 steps is {difference}",
        part=1,
    )
    io_handler.set_solution(solution)
    character_count = extension.character_count_after_multiple_extensions(
        polymer, num_times=40
    )
    difference = max(character_count.values()) - min(character_count.values())
    solution = ProblemSolution(
        problem_id,
        f"The difference between the most and least common characters after 40 steps is {difference}",
        part=2,
    )
    io_handler.set_solution(solution)
