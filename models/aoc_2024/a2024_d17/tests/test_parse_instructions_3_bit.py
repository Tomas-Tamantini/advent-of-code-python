from ..logic.instructions_3_bit import (
    Division3BitInstruction,
    JumpNotZero3BitInstruction,
    Modulo3BitInstruction,
    Output3BitInstruction,
    XorLiteral3BitInstruction,
    XorRegisters3BitInstruction,
)
from ..logic.parse_instructions_3_bit import parse_3_bit_instruction


def test_parse_adv_3_bit_instruction():
    assert parse_3_bit_instruction(op_code=0, operand=3) == Division3BitInstruction(
        numerator_register="A", output_register="A", operand=3
    )


def test_parse_bxl_3_bit_instruction():
    assert parse_3_bit_instruction(op_code=1, operand=3) == XorLiteral3BitInstruction(
        register="B", literal=3
    )


def test_parse_bst_3_bit_instruction():
    assert parse_3_bit_instruction(op_code=2, operand=3) == Modulo3BitInstruction(
        output_register="B", operand=3, modulo=8
    )


def test_parse_jnz_3_bit_instruction():
    assert parse_3_bit_instruction(op_code=3, operand=3) == JumpNotZero3BitInstruction(
        register="A", new_pc=3
    )


def test_parse_bxc_3_bit_instruction():
    assert parse_3_bit_instruction(op_code=4, operand=3) == XorRegisters3BitInstruction(
        register_a="B", register_b="C"
    )


def test_parse_out_3_bit_instruction():
    assert parse_3_bit_instruction(op_code=5, operand=3) == Output3BitInstruction(
        operand=3, modulo=8
    )


def test_parse_bdv_3_bit_instruction():
    assert parse_3_bit_instruction(op_code=6, operand=3) == Division3BitInstruction(
        numerator_register="A", output_register="B", operand=3
    )


def test_parse_cdv_3_bit_instruction():
    assert parse_3_bit_instruction(op_code=7, operand=3) == Division3BitInstruction(
        numerator_register="A", output_register="C", operand=3
    )
