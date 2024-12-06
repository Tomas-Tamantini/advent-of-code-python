from typing import Iterator

from models.common.assembly import Instruction
from models.common.io import InputReader

from .logic import IncrementGlobalAccumulatorInstruction, JumpOrNoOpInstruction


def _parse_game_console_instruction(instruction: str) -> Instruction:
    parts = instruction.split()
    operation = parts[0].strip()
    value = int(parts[1])
    if operation == "nop":
        return JumpOrNoOpInstruction(offset=value, is_jump=False)
    elif operation == "acc":
        return IncrementGlobalAccumulatorInstruction(increment=value)
    elif operation == "jmp":
        return JumpOrNoOpInstruction(offset=value, is_jump=True)
    else:
        raise ValueError(f"Unknown instruction: {instruction}")


def parse_game_console_instructions(input_reader: InputReader) -> Iterator[Instruction]:
    for line in input_reader.read_stripped_lines():
        yield _parse_game_console_instruction(line)
