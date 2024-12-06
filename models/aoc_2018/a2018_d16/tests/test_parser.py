from unittest.mock import Mock

from models.common.io import InputFromString

from ..parser import parse_instruction_samples, parse_unknown_op_code_program
from ..unknown_op_code import InstructionSample


def test_parse_instruction_samples():
    file_content = """Before: [1, 2, 3, 4]
                      123 1 2 3
                      After:  [4, 3, 2, 1]

                      Before: [10, 20, 30, 40]
                      321 3 2 1
                      After:  [40, 30, 20, 10]
                      Line to ignore"""
    samples = list(parse_instruction_samples(InputFromString(file_content)))
    assert samples == [
        InstructionSample(
            op_code=123,
            instruction_values=(1, 2, 3),
            registers_before=(1, 2, 3, 4),
            registers_after=(4, 3, 2, 1),
        ),
        InstructionSample(
            op_code=321,
            instruction_values=(3, 2, 1),
            registers_before=(10, 20, 30, 40),
            registers_after=(40, 30, 20, 10),
        ),
    ]


def test_parse_unknown_op_code_program():
    file_content = """After:  [40, 30, 20, 10]

                      14 1 2 3
                      13 3 2 1"""
    instruction_a_spy = Mock()
    instruction_b_spy = Mock()
    op_code_to_instruction = {
        14: instruction_a_spy,
        13: instruction_b_spy,
    }
    instructions = list(
        parse_unknown_op_code_program(
            InputFromString(file_content), op_code_to_instruction
        )
    )
    assert instructions == [
        instruction_a_spy(1, 2, 3),
        instruction_b_spy(3, 2, 1),
    ]
