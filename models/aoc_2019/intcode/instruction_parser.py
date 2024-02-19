from typing import Iterator
from models.assembly import Instruction
from .instructions import (
    ParameterMode,
    IntcodeParameter,
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


def _parse_parameter_modes(op_code: int) -> list[ParameterMode]:
    op_code_str = str(op_code)
    if len(op_code_str) <= 2:
        return []
    else:
        return [ParameterMode(int(digit)) for digit in reversed(op_code_str[:-2])]


def _build_parameters(
    num_parameters: int, sequence: list[int]
) -> Iterator[IntcodeParameter]:
    parameter_modes = _parse_parameter_modes(sequence[0])
    for i in range(num_parameters):
        parameter_mode = (
            parameter_modes[i] if i < len(parameter_modes) else ParameterMode.POSITION
        )
        yield IntcodeParameter(value=sequence[i + 1], parameter_mode=parameter_mode)


def parse_next_instruction(sequence: list[int]) -> Instruction:
    op_code = _parse_op_code(sequence[0])
    instruction, num_params = {
        99: (IntcodeHalt, 0),
        1: (IntcodeAdd, 3),
        2: (IntcodeMultiply, 3),
        3: (IntcodeInput, 1),
        4: (IntcodeOutput, 1),
        5: (IntcodeJumpIfTrue, 2),
        6: (IntcodeJumpIfFalse, 2),
        7: (IntcodeLessThan, 3),
        8: (IntcodeEquals, 3),
    }[op_code]
    parameters = _build_parameters(num_params, sequence)
    return instruction(*parameters)
