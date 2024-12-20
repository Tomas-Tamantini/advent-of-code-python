from typing import Callable, Iterator

from models.common.io import IOHandler, Problem, ProblemSolution


def follow_and_increment_jump_instructions(
    jump_instructions: list[int], increment_rule: Callable[[int], int]
) -> Iterator[int]:
    current_pos = 0
    while 0 <= current_pos < len(jump_instructions):
        yield current_pos
        jump = jump_instructions[current_pos]
        jump_instructions[current_pos] = increment_rule(jump)
        current_pos += jump


def aoc_2017_d5(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 5, "A Maze of Twisty Trampolines, All Alike")
    io_handler.output_writer.write_header(problem_id)
    jump_offsets = [int(line) for line in io_handler.input_reader.readlines()]
    steps_simple_increment = 0
    for _ in follow_and_increment_jump_instructions(
        jump_offsets[:], increment_rule=lambda jump: jump + 1
    ):
        steps_simple_increment += 1
    yield ProblemSolution(
        problem_id,
        f"Steps to exit with simple increment: {steps_simple_increment}",
        part=1,
        result=steps_simple_increment,
    )

    steps_complex_increment = 0
    for _ in follow_and_increment_jump_instructions(
        jump_offsets[:], increment_rule=lambda jump: jump - 1 if jump >= 3 else jump + 1
    ):
        steps_complex_increment += 1
    yield ProblemSolution(
        problem_id,
        f"Steps to exit with increment/decrement: {steps_complex_increment}",
        part=2,
        result=steps_complex_increment,
    )
