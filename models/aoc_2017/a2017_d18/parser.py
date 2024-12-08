from typing import Iterator

from models.common.assembly import (
    AddInstruction,
    CopyInstruction,
    Instruction,
    JumpGreaterThanZeroInstruction,
    JumpNotZeroInstruction,
    OutInstruction,
    SubtractInstruction,
)
from models.common.io import InputReader

from .duet_code import (
    MultiplyInstruction,
    RecoverLastFrequencyInstruction,
    RemainderInstruction,
)


def _parse_instruction_parts(instruction_str: str) -> list[int | str]:
    raw_parts = instruction_str.split(" ")
    parts = []
    for part in raw_parts[1:]:
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(part)
    return parts


def parse_duet_instruction(instruction_str: str, rcv_cls, mul_cls) -> Instruction:
    parts = _parse_instruction_parts(instruction_str)
    instruction_map = {
        "snd": lambda p: OutInstruction(source=p[0]),
        "set": lambda p: CopyInstruction(source=p[1], destination=p[0]),
        "add": lambda p: AddInstruction(source=p[1], destination=p[0]),
        "sub": lambda p: SubtractInstruction(source=p[1], destination=p[0]),
        "mul": lambda p: mul_cls(p[1], p[0]),
        "mod": lambda p: RemainderInstruction(source=p[1], destination=p[0]),
        "rcv": lambda p: rcv_cls(p[0]),
        "jgz": lambda p: JumpGreaterThanZeroInstruction(
            value_to_compare=p[0],
            offset=p[1],
        ),
        "jnz": lambda p: JumpNotZeroInstruction(
            value_to_compare=p[0],
            offset=p[1],
        ),
    }
    return instruction_map[instruction_str[:3]](parts)


def parse_duet_code(
    input_reader: InputReader,
    rcv_cls=RecoverLastFrequencyInstruction,
    mul_cls=MultiplyInstruction,
) -> Iterator[Instruction]:
    for line in input_reader.read_stripped_lines():
        yield parse_duet_instruction(line, rcv_cls, mul_cls)
