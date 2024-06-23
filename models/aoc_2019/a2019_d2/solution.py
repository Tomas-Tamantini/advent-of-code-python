from models.common.io import IOHandler
from .noun_and_verb import (
    run_intcode_program_until_halt,
    noun_and_verb_for_given_output,
)


def aoc_2019_d2(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2019 - Day 2: 1202 Program Alarm ---")
    original_instructions = [
        int(code) for code in io_handler.input_reader.read().split(",")
    ]
    instructions = original_instructions[:]
    instructions[1] = 12
    instructions[2] = 2
    final_state = run_intcode_program_until_halt(instructions)
    print(f"Part 1: Value at position 0 is {final_state[0]}")
    noun, verb = noun_and_verb_for_given_output(
        original_instructions, desired_output=19690720, noun_range=100, verb_range=100
    )
    combined = 100 * noun + verb
    print(f"Part 2: Noun and verb combined is {combined}")
