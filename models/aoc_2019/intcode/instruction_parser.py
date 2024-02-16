from typing import Iterator
from models.assembly import Instruction
from .instructions import (
    MemoryOrImmediate,
    IntcodeHalt,
    IntcodeAdd,
    IntcodeMultiply,
    IntcodeInput,
    IntcodeOutput,
    IntcodeJumpIfTrue,
    IntcodeJumpIfFalse,
    IntcodeLessThan,
    IntcodeEquals,
)


def _parse_op_code(op_code: int) -> int:
    op_code_str = str(op_code)
    if len(op_code_str) <= 2:
        return op_code
    else:
        return int(op_code_str[-2:])


def _parse_parameter_modes(op_code: int) -> list[int]:
    op_code_str = str(op_code)
    if len(op_code_str) <= 2:
        return []
    else:
        return [int(digit) for digit in reversed(op_code_str[:-2])]


def _build_parameters(sequence: list[int]) -> Iterator[MemoryOrImmediate]:
    op_code = _parse_op_code(sequence[0])
    num_parameters = {1: 2, 2: 2, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2}.get(op_code, 0)
    parameter_modes = _parse_parameter_modes(sequence[0])
    for i in range(num_parameters):
        is_memory = i >= len(parameter_modes) or parameter_modes[i] == 0
        yield MemoryOrImmediate(value=sequence[i + 1], is_memory=is_memory)


def parse_next_instruction(sequence: list[int]) -> Instruction:
    op_code = _parse_op_code(sequence[0])
    parameters = _build_parameters(sequence)
    if op_code == 99:
        return IntcodeHalt()
    elif op_code == 1:
        return IntcodeAdd(*parameters, output=sequence[3])
    elif op_code == 2:
        return IntcodeMultiply(*parameters, output=sequence[3])
    elif op_code == 3:
        return IntcodeInput(output=sequence[1])
    elif op_code == 4:
        return IntcodeOutput(*parameters)
    elif op_code == 5:
        return IntcodeJumpIfTrue(*parameters)
    elif op_code == 6:
        return IntcodeJumpIfFalse(*parameters)
    elif op_code == 7:
        return IntcodeLessThan(*parameters, output=sequence[3])
    elif op_code == 8:
        return IntcodeEquals(*parameters, output=sequence[3])
    else:
        raise ValueError(f"Invalid opcode: {sequence[0]}")
