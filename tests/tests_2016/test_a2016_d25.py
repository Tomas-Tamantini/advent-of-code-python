import pytest
from models.assembly import CopyInstruction, OutInstruction, JumpNotZeroInstruction
from models.aoc_2016 import (
    smallest_value_to_send_clock_signal,
    AssembunnyProgram,
    IncrementInstruction,
    DecrementInstruction,
)


@pytest.mark.skip(reason="Takes about 3s to run")
def test_smallest_value_to_send_clock_signal_is_calculated_properly():
    program = AssembunnyProgram(
        [
            CopyInstruction("a", "d"),
            CopyInstruction(7, "c"),
            CopyInstruction(365, "b"),
            IncrementInstruction("d"),
            DecrementInstruction("b"),
            JumpNotZeroInstruction(value_to_compare="b", offset=-2),
            DecrementInstruction("c"),
            JumpNotZeroInstruction(value_to_compare="c", offset=-5),
            CopyInstruction("d", "a"),
            JumpNotZeroInstruction(value_to_compare=0, offset=0),
            CopyInstruction("a", "b"),
            CopyInstruction(0, "a"),
            CopyInstruction(2, "c"),
            JumpNotZeroInstruction(value_to_compare="b", offset=2),
            JumpNotZeroInstruction(value_to_compare=1, offset=6),
            DecrementInstruction("b"),
            DecrementInstruction("c"),
            JumpNotZeroInstruction(value_to_compare="c", offset=-4),
            IncrementInstruction("a"),
            JumpNotZeroInstruction(value_to_compare=1, offset=-7),
            CopyInstruction(2, "b"),
            JumpNotZeroInstruction(value_to_compare="c", offset=2),
            JumpNotZeroInstruction(value_to_compare=1, offset=4),
            DecrementInstruction("b"),
            DecrementInstruction("c"),
            JumpNotZeroInstruction(value_to_compare=1, offset=-4),
            JumpNotZeroInstruction(value_to_compare=0, offset=0),
            OutInstruction("b"),
            JumpNotZeroInstruction(value_to_compare="a", offset=-19),
            JumpNotZeroInstruction(value_to_compare=1, offset=-21),
        ]
    )
    assert smallest_value_to_send_clock_signal(program) == 175
