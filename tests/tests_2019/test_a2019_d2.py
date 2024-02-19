import pytest
from models.aoc_2019 import (
    run_intcode_program_until_halt,
    noun_and_verb_for_given_output,
)


def test_running_intcode_program_leaves_initial_instructions_intact():
    instructions = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    _ = run_intcode_program_until_halt(instructions)
    assert instructions == [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]


@pytest.mark.parametrize(
    "instructions, expected",
    [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        (
            [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50],
            [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
        ),
    ],
)
def test_running_intcode_program_yields_final_state(instructions, expected):
    assert run_intcode_program_until_halt(instructions) == expected


def test_can_find_noun_and_verb_that_yield_desired_output():
    instructions = [1, -1, -1, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    noun, verb = noun_and_verb_for_given_output(
        instructions, 3500, noun_range=15, verb_range=15
    )
    assert noun == 10
    assert verb == 9
