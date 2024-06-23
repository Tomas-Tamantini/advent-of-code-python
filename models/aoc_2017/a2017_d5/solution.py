from typing import Iterator, Callable
from models.common.io import IOHandler


def follow_and_increment_jump_instructions(
    jump_instructions: list[int], increment_rule: Callable[[int], int]
) -> Iterator[int]:
    current_pos = 0
    while 0 <= current_pos < len(jump_instructions):
        yield current_pos
        jump = jump_instructions[current_pos]
        jump_instructions[current_pos] = increment_rule(jump)
        current_pos += jump


def aoc_2017_d5(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(
        2017, 5, "A Maze of Twisty Trampolines, All Alike"
    )
    jump_offsets = [int(line) for line in io_handler.input_reader.readlines()]
    simple_increment_rule = lambda jump: jump + 1
    steps_simple_increment = 0
    for _ in follow_and_increment_jump_instructions(
        jump_offsets[:], simple_increment_rule
    ):
        steps_simple_increment += 1
    print(f"Part 1: Steps to exit with simple increment: {steps_simple_increment}")
    complex_increment_rule = lambda jump: jump - 1 if jump >= 3 else jump + 1
    steps_complex_increment = 0
    for _ in follow_and_increment_jump_instructions(
        jump_offsets[:], complex_increment_rule
    ):
        steps_complex_increment += 1
    print(f"Part 2: Steps to exit with increment/decrement: {steps_complex_increment}")
