from typing import Iterable, Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .brackets import mismatching_brackets, missing_brackets


def aoc_2021_d10(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2021, 10, "Syntax Scoring")
    io_handler.output_writer.write_header(problem_id)
    mismatch_scores = {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }
    lines = [line.strip() for line in io_handler.input_reader.readlines()]

    incomplete_lines = []

    mismatch_score = 0
    for line in lines:
        try:
            mismatch = next(mismatching_brackets(line))
            mismatch_score += mismatch_scores[mismatch]
        except StopIteration:
            incomplete_lines.append(line)
    yield ProblemSolution(
        problem_id,
        f"The total mismatch score is {mismatch_score}",
        part=1,
        result=mismatch_score,
    )

    def missing_score(missing_brackets: Iterable[chr]) -> int:
        missing_scores = {
            ")": 1,
            "]": 2,
            "}": 3,
            ">": 4,
        }
        score = 0
        for missing in missing_brackets:
            score = score * 5 + missing_scores[missing]
        return score

    missing_scores = [
        missing_score(missing_brackets(line)) for line in incomplete_lines
    ]

    middle_score = sorted(missing_scores)[len(missing_scores) // 2]
    yield ProblemSolution(
        problem_id,
        f"The middle missing score is {middle_score}",
        part=2,
        result=middle_score,
    )
