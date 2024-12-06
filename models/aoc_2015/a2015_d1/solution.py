from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution


def final_floor(instructions: str) -> int:
    return instructions.count("(") - instructions.count(")")


def first_basement(instructions: str) -> int:
    floor = 0
    for i, c in enumerate(instructions, 1):
        floor += 1 if c == "(" else -1
        if floor == -1:
            return i
    return -1


def aoc_2015_d1(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2015, 1, "Not Quite Lisp")
    io_handler.output_writer.write_header(problem_id)
    instructions = io_handler.input_reader.read()

    floor = final_floor(instructions)
    yield ProblemSolution(
        problem_id, f"Santa is on floor {floor}", part=1, result=floor
    )

    basement = first_basement(instructions)
    yield ProblemSolution(
        problem_id,
        f"Santa first enters the basement at instruction {basement}",
        part=2,
        result=basement,
    )
