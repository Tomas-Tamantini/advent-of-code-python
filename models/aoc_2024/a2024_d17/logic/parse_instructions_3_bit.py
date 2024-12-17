from models.common.assembly import Instruction

from .instructions_3_bit import (
    Division3BitInstruction,
    JumpNotZero3BitInstruction,
    Modulo3BitInstruction,
    Output3BitInstruction,
    XorLiteral3BitInstruction,
    XorRegisters3BitInstruction,
)


def parse_3_bit_instruction(op_code: int, operand: int) -> Instruction:
    return {
        0: lambda op: Division3BitInstruction("A", "A", op),
        1: lambda op: XorLiteral3BitInstruction("B", op),
        2: lambda op: Modulo3BitInstruction("B", op, 8),
        3: lambda op: JumpNotZero3BitInstruction("A", op),
        4: lambda op: XorRegisters3BitInstruction("B", "C"),
        5: lambda op: Output3BitInstruction(op, 8),
        6: lambda op: Division3BitInstruction("A", "B", op),
        7: lambda op: Division3BitInstruction("A", "C", op),
    }[op_code](operand)
