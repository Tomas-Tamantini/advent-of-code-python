import pytest
from models.aoc_2016 import (
    smallest_value_to_send_clock_signal,
    Program,
    CopyInstruction,
    IncrementInstruction,
    DecrementInstruction,
    JumpNotZeroInstruction,
    OutInstruction,
)


@pytest.mark.skip(reason="Takes about 3s to run")
def test_smallest_value_to_send_clock_signal_is_calculated_properly():
    program = Program(
        [
            CopyInstruction("a", "d"),
            CopyInstruction(7, "c"),
            CopyInstruction(365, "b"),
            IncrementInstruction("d"),
            DecrementInstruction("b"),
            JumpNotZeroInstruction("b", -2),
            DecrementInstruction("c"),
            JumpNotZeroInstruction("c", -5),
            CopyInstruction("d", "a"),
            JumpNotZeroInstruction(0, 0),
            CopyInstruction("a", "b"),
            CopyInstruction(0, "a"),
            CopyInstruction(2, "c"),
            JumpNotZeroInstruction("b", 2),
            JumpNotZeroInstruction(1, 6),
            DecrementInstruction("b"),
            DecrementInstruction("c"),
            JumpNotZeroInstruction("c", -4),
            IncrementInstruction("a"),
            JumpNotZeroInstruction(1, -7),
            CopyInstruction(2, "b"),
            JumpNotZeroInstruction("c", 2),
            JumpNotZeroInstruction(1, 4),
            DecrementInstruction("b"),
            DecrementInstruction("c"),
            JumpNotZeroInstruction(1, -4),
            JumpNotZeroInstruction(0, 0),
            OutInstruction("b"),
            JumpNotZeroInstruction("a", -19),
            JumpNotZeroInstruction(1, -21),
        ]
    )
    assert smallest_value_to_send_clock_signal(program) == 175
