import pytest

from ..logic import Program3Bit, SerialOutput3Bit, run_3_bit_program
from ..logic.instructions_3_bit import JumpNotZero3BitInstruction, Modulo3BitInstruction


def test_3_bit_program_returns_none_if_pc_outside_its_range():
    program = Program3Bit((3, 2, 1))
    assert program.get_instruction(3) is None
    assert program.get_instruction(-1) is None


def test_3_bit_program_returns_parsed_instruction_if_pc_within_range():
    program = Program3Bit((3, 2, 1))
    assert program.get_instruction(0) == JumpNotZero3BitInstruction(
        register="A", new_pc=2
    )
    assert program.get_instruction(1) == Modulo3BitInstruction(
        output_register="B", operand=1, modulo=8
    )


@pytest.mark.parametrize(
    ("instructions", "register_a", "expected_output"),
    [
        ((5, 0, 5, 1, 5, 4), 10, "0,1,2"),
        ((0, 1, 5, 4, 3, 0), 2024, "4,2,5,6,7,7,7,7,3,1,0"),
        ((0, 1, 5, 4, 3, 0), 729, "4,6,3,5,6,3,5,2,1,0"),
        ((0, 3, 5, 4, 3, 0), 117440, "0,3,5,4,3,0"),
    ],
)
def test_3_bit_program_runs_until_halting(instructions, register_a, expected_output):
    registers = {"A": register_a, "B": 0, "C": 0}
    program = Program3Bit(instructions)
    output = SerialOutput3Bit()
    run_3_bit_program(program, output, registers)
    assert expected_output == output.get_output()
