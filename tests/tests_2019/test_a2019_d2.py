import pytest
from models.aoc_2019 import run_intcode_program_until_halt


def test_running_intcode_program_leaves_initial_sequence_intact():
    sequence = [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]
    _ = run_intcode_program_until_halt(sequence)
    assert sequence == [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]


@pytest.mark.parametrize(
    "sequence, expected",
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
def test_running_intcode_program_yields_final_state(sequence, expected):
    assert run_intcode_program_until_halt(sequence) == expected
