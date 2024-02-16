from models.assembly import Instruction
from .instructions import (
    MemoryOrImmediate,
    IntcodeHalt,
    IntcodeAdd,
    IntcodeMultiply,
    IntcodeInput,
    IntcodeOutput,
)


def parse_next_instruction(sequence: list[int]) -> Instruction:
    if sequence[0] == 99:
        return IntcodeHalt()
    elif sequence[0] == 1:
        return IntcodeAdd(
            input_a=MemoryOrImmediate(
                value=sequence[1],
                is_memory=True,
            ),
            input_b=MemoryOrImmediate(
                value=sequence[2],
                is_memory=True,
            ),
            output=sequence[3],
        )
    elif sequence[0] == 2:
        return IntcodeMultiply(
            input_a=MemoryOrImmediate(
                value=sequence[1],
                is_memory=True,
            ),
            input_b=MemoryOrImmediate(
                value=sequence[2],
                is_memory=True,
            ),
            output=sequence[3],
        )
    elif sequence[0] == 3:
        return IntcodeInput(
            output=sequence[1],
        )
    elif sequence[0] == 4:
        return IntcodeOutput(
            value=MemoryOrImmediate(
                value=sequence[1],
                is_memory=True,
            ),
        )
    else:
        raise ValueError(f"Invalid opcode: {sequence[0]}")
