import pytest
from models.assembly import Hardware, Processor
from models.aoc_2017 import (
    ComparisonOperator,
    ConditionalIncrementInstruction,
    registers_after_conditional_increment_instructions,
)


@pytest.mark.parametrize(
    "comparison_operator, value_to_compare",
    [
        (ComparisonOperator.EQUALS, 1),
        (ComparisonOperator.NOT_EQUALS, 10),
        (ComparisonOperator.GREATER_THAN, 10),
        (ComparisonOperator.LESS_THAN, 10),
        (ComparisonOperator.GREATER_THAN_OR_EQUAL, 11),
        (ComparisonOperator.LESS_THAN_OR_EQUAL, 9),
    ],
)
def test_instruction_just_updates_program_counter_when_comparison_fails(
    comparison_operator, value_to_compare
):
    processor = Processor(program_counter=10, registers={"a": 5, "b": 10})
    hardware = Hardware(processor)
    instruction = ConditionalIncrementInstruction(
        register_to_increment="a",
        increment_amount=1,
        comparison_register="b",
        value_to_compare=value_to_compare,
        comparison_operator=comparison_operator,
    )
    instruction.execute(hardware)
    assert processor.program_counter == 11
    assert processor.registers["a"] == 5


@pytest.mark.parametrize(
    "comparison_operator, value_to_compare",
    [
        (ComparisonOperator.EQUALS, 10),
        (ComparisonOperator.NOT_EQUALS, 1),
        (ComparisonOperator.GREATER_THAN, 9),
        (ComparisonOperator.LESS_THAN, 11),
        (ComparisonOperator.GREATER_THAN_OR_EQUAL, 10),
        (ComparisonOperator.LESS_THAN_OR_EQUAL, 10),
    ],
)
def test_instruction_updates_programs_counter_and_increments_register_when_comparison_is_true(
    comparison_operator, value_to_compare
):
    processor = Processor(program_counter=10, registers={"a": 5, "b": 10})
    hardware = Hardware(processor)
    instruction = ConditionalIncrementInstruction(
        register_to_increment="a",
        increment_amount=2,
        comparison_register="b",
        value_to_compare=value_to_compare,
        comparison_operator=comparison_operator,
    )
    instruction.execute(hardware)
    assert processor.program_counter == 11
    assert processor.registers["a"] == 7


def test_can_run_program_and_check_register_values_afterwards():
    program = [
        ConditionalIncrementInstruction(
            "b", 5, "a", 1, ComparisonOperator.GREATER_THAN
        ),
        ConditionalIncrementInstruction("a", 1, "b", 5, ComparisonOperator.LESS_THAN),
        ConditionalIncrementInstruction(
            "c", 10, "a", 1, ComparisonOperator.GREATER_THAN_OR_EQUAL
        ),
        ConditionalIncrementInstruction("c", -20, "c", 10, ComparisonOperator.EQUALS),
    ]
    registers = registers_after_conditional_increment_instructions(program)
    assert registers == {"a": 1, "b": 0, "c": -10}
