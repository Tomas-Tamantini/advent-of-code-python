from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import LineOfReflection, ReflectionOrientation, find_line_of_reflection
from .parser import parse_ash_valleys


def _line_of_reflection_summary(line_of_reflection: LineOfReflection) -> int:
    summary = line_of_reflection.line_index + 1
    return (
        summary
        if line_of_reflection.orientation == ReflectionOrientation.VERTICAL
        else 100 * summary
    )


def aoc_2023_d13(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 13, "Point of Incidence")
    io_handler.output_writer.write_header(problem_id)
    valleys = list(parse_ash_valleys(io_handler.input_reader))

    summary_no_mismatch = sum(
        _line_of_reflection_summary(find_line_of_reflection(valley, num_mismatches=0))
        for valley in valleys
    )
    yield ProblemSolution(
        problem_id,
        f"Summary of reflection lines with no mismatches is {summary_no_mismatch}",
        result=summary_no_mismatch,
        part=1,
    )

    summary_one_mismatch = sum(
        _line_of_reflection_summary(find_line_of_reflection(valley, num_mismatches=1))
        for valley in valleys
    )
    yield ProblemSolution(
        problem_id,
        f"Summary of reflection lines with one mismatch is {summary_one_mismatch}",
        result=summary_one_mismatch,
        part=2,
    )
