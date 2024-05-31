from typing import Iterator
from models.common.io import InputReader
from models.common.assembly import (
    Instruction,
    CopyInstruction,
    OutInstruction,
    JumpNotZeroInstruction,
    JumpGreaterThanZeroInstruction,
    AddInstruction,
    SubtractInstruction,
)
from .duet_code import (
    MultiplyInstruction,
    RemainderInstruction,
    RecoverLastFrequencyInstruction,
)


def parse_duet_instruction(instruction_str: str, rcv_cls, mul_cls) -> Instruction:
    raw_parts = instruction_str.split(" ")
    parts = []
    for part in raw_parts[1:]:
        try:
            parts.append(int(part))
        except ValueError:
            parts.append(part)
    if "snd" in instruction_str:
        return OutInstruction(source=parts[0])
    elif "set" in instruction_str:
        return CopyInstruction(source=parts[1], destination=parts[0])
    elif "add" in instruction_str:
        return AddInstruction(source=parts[1], destination=parts[0])
    elif "sub" in instruction_str:
        return SubtractInstruction(source=parts[1], destination=parts[0])
    elif "mul" in instruction_str:
        return mul_cls(parts[1], parts[0])
    elif "mod" in instruction_str:
        return RemainderInstruction(source=parts[1], destination=parts[0])
    elif "rcv" in instruction_str:
        return rcv_cls(parts[0])
    elif "jgz" in instruction_str:
        return JumpGreaterThanZeroInstruction(
            value_to_compare=parts[0],
            offset=parts[1],
        )
    elif "jnz" in instruction_str:
        return JumpNotZeroInstruction(
            value_to_compare=parts[0],
            offset=parts[1],
        )
    else:
        raise ValueError(f"Unknown instruction: {instruction_str}")


def parse_duet_code(
    input_reader: InputReader,
    rcv_cls=RecoverLastFrequencyInstruction,
    mul_cls=MultiplyInstruction,
) -> Iterator[Instruction]:
    for line in input_reader.read_stripped_lines():
        yield parse_duet_instruction(line, rcv_cls, mul_cls)
