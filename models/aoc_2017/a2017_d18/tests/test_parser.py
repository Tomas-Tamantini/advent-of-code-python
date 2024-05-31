from dataclasses import dataclass
from models.common.io import InputFromString
from models.common.assembly import (
    CopyInstruction,
    InputInstruction,
    OutInstruction,
    JumpNotZeroInstruction,
    JumpGreaterThanZeroInstruction,
    AddInstruction,
    SubtractInstruction,
)
from ..duet_code import (
    MultiplyInstruction,
    RemainderInstruction,
    RecoverLastFrequencyInstruction,
)
from ..parser import parse_duet_code


def test_parse_duet_code():
    file_content = """set a 1
                      add a 2
                      mul a b
                      mod a 5
                      snd a
                      set a 0
                      rcv a
                      jgz a -1"""
    instructions = list(parse_duet_code(InputFromString(file_content)))
    assert len(instructions) == 8
    assert instructions[0] == CopyInstruction(1, "a")
    assert instructions[1] == AddInstruction(2, "a")
    assert instructions[2] == MultiplyInstruction("b", "a")
    assert instructions[3] == RemainderInstruction(5, "a")
    assert instructions[4] == OutInstruction("a")
    assert instructions[5] == CopyInstruction(0, "a")
    assert instructions[6] == RecoverLastFrequencyInstruction("a")
    assert instructions[7] == JumpGreaterThanZeroInstruction(-1, "a")


def test_parse_duet_code_with_rcv_as_input_instruction():
    file_content = "rcv a"
    instructions = list(
        parse_duet_code(InputFromString(file_content), rcv_cls=InputInstruction)
    )
    assert instructions == [InputInstruction("a")]


def test_parse_duet_code_with_spy_multiply():
    file_content = """mul a b
                      jnz a -1
                      sub b -6"""

    @dataclass(frozen=True)
    class _MockMultiply:
        source: int
        destination: str

    instructions = list(
        parse_duet_code(InputFromString(file_content), mul_cls=_MockMultiply)
    )
    assert instructions == [
        _MockMultiply("b", "a"),
        JumpNotZeroInstruction(-1, "a"),
        SubtractInstruction(source=-6, destination="b"),
    ]
