from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .noun_and_verb import (
    run_intcode_program_until_halt,
    noun_and_verb_for_given_output,
)


def aoc_2019_d2(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 2, "1202 Program Alarm")
    io_handler.output_writer.write_header(problem_id)
    original_instructions = [
        int(code) for code in io_handler.input_reader.read().split(",")
    ]
    instructions = original_instructions[:]
    instructions[1] = 12
    instructions[2] = 2
    final_state = run_intcode_program_until_halt(instructions)
    yield ProblemSolution(
        problem_id, f"Value at position 0 is {final_state[0]}", part=1
    )

    noun, verb = noun_and_verb_for_given_output(
        original_instructions, desired_output=19690720, noun_range=100, verb_range=100
    )
    combined = 100 * noun + verb
    yield ProblemSolution(problem_id, f"Noun and verb combined is {combined}", part=2)
