from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .parser import parse_polymer_and_polymer_extension_rules
from .polymer_extension import PolymerExtension


def aoc_2021_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 14, "Extended Polymerization")
    io_handler.output_writer.write_header(problem_id)
    polymer, rules = parse_polymer_and_polymer_extension_rules(io_handler.input_reader)
    extension = PolymerExtension(rules)
    character_count = extension.character_count_after_multiple_extensions(
        polymer, num_times=10
    )
    result = max(character_count.values()) - min(character_count.values())
    yield ProblemSolution(
        problem_id,
        (
            "The difference between the most and least common characters "
            f"after 10 steps is {result}"
        ),
        result,
        part=1,
    )

    character_count = extension.character_count_after_multiple_extensions(
        polymer, num_times=40
    )
    result = max(character_count.values()) - min(character_count.values())
    yield ProblemSolution(
        problem_id,
        (
            "The difference between the most and least common characters "
            f"after 40 steps is {result}"
        ),
        result,
        part=2,
    )
