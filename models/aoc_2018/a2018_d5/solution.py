from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .polymer_reaction import polymer_reaction, minimum_polymer_length


def aoc_2018_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2018, 5, "Alchemical Reduction")
    io_handler.output_writer.write_header(problem_id)
    polymer = io_handler.input_reader.read().strip()
    reacted_polymer = polymer_reaction(polymer)
    yield ProblemSolution(
        problem_id,
        f"Length of reacted polymer: {len(reacted_polymer)}",
        part=1,
        result=len(reacted_polymer),
    )

    result = minimum_polymer_length(polymer)
    yield ProblemSolution(
        problem_id, f"Minimum length of polymer: {result}", result, part=2
    )
