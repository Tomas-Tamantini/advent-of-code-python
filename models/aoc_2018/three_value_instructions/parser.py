from typing import Iterator
from models.common.io import InputReader
from .instructions import (
    AddRegisters,
    AddImmediate,
    MultiplyRegisters,
    MultiplyImmediate,
    BitwiseAndRegisters,
    BitwiseAndImmediate,
    BitwiseOrRegisters,
    BitwiseOrImmediate,
    AssignmentRegisters,
    AssignmentImmediate,
    GreaterThanImmediateRegister,
    GreaterThanRegisterImmediate,
    GreaterThanRegisterRegister,
    EqualImmediateRegister,
    EqualRegisterImmediate,
    EqualRegisterRegister,
    ThreeValueInstruction,
)


def parse_three_value_instructions(
    input_reader: InputReader,
) -> Iterator[ThreeValueInstruction]:
    register_bound_to_pc = None
    instruction_types = {
        "addr": AddRegisters,
        "addi": AddImmediate,
        "mulr": MultiplyRegisters,
        "muli": MultiplyImmediate,
        "banr": BitwiseAndRegisters,
        "bani": BitwiseAndImmediate,
        "borr": BitwiseOrRegisters,
        "bori": BitwiseOrImmediate,
        "setr": AssignmentRegisters,
        "seti": AssignmentImmediate,
        "gtir": GreaterThanImmediateRegister,
        "gtri": GreaterThanRegisterImmediate,
        "gtrr": GreaterThanRegisterRegister,
        "eqir": EqualImmediateRegister,
        "eqri": EqualRegisterImmediate,
        "eqrr": EqualRegisterRegister,
    }
    for line in input_reader.readlines():
        parts = line.strip().split()
        if "#ip" in parts:
            register_bound_to_pc = int(parts[-1])
        else:
            instruction_type = instruction_types[parts[0]]
            yield instruction_type(*map(int, parts[1:]), register_bound_to_pc)
