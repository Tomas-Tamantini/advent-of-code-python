from models.aoc_2018.three_value_instructions import (
    ALL_THREE_VALUE_INSTRUCTIONS,
    AddImmediate,
    AssignmentImmediate,
    MultiplyRegisters,
)

from ..unknown_op_code import (
    InstructionSample,
    possible_instructions,
    work_out_op_codes,
)


def test_can_figure_out_what_instructions_produce_given_outcome():
    registers_before = [3, 2, 1, 1]
    registers_after = [3, 2, 2, 1]
    instruction_values = (2, 1, 2)
    instruction_sample = InstructionSample(
        op_code=9,
        instruction_values=instruction_values,
        registers_before=registers_before,
        registers_after=registers_after,
    )
    candidates = ALL_THREE_VALUE_INSTRUCTIONS
    expected = [AddImmediate, MultiplyRegisters, AssignmentImmediate]
    actual = list(possible_instructions(instruction_sample, candidates))
    assert actual == expected


def test_can_figure_out_instructions_op_code_exactly_from_multiple_samples():
    samples = [
        InstructionSample(
            op_code=1,
            instruction_values=(2, 1, 2),
            registers_before=[3, 2, 1, 1],
            registers_after=[3, 2, 2, 1],
        ),
        InstructionSample(
            op_code=2,
            instruction_values=(2, 1, 2),
            registers_before=[3, 2, 1, 1],
            registers_after=[3, 2, 2, 1],
        ),
        InstructionSample(
            op_code=2,
            instruction_values=(1, 2, 0),
            registers_before=[3, 5, 7, 11],
            registers_after=[35, 5, 7, 11],
        ),
        InstructionSample(
            op_code=3,
            instruction_values=(12345, 2, 0),
            registers_before=[3, 5, 7, 11],
            registers_after=[12345, 5, 7, 11],
        ),
    ]
    worked_out_op_codes = work_out_op_codes(
        samples, candidates=ALL_THREE_VALUE_INSTRUCTIONS
    )
    assert worked_out_op_codes == {
        1: AddImmediate,
        2: MultiplyRegisters,
        3: AssignmentImmediate,
    }
