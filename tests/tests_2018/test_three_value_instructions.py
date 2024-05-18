import pytest
from models.common.assembly import Hardware, Processor
from models.aoc_2018.three_value_instructions import (
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
    ALL_THREE_VALUE_INSTRUCTIONS,
    ThreeValueInstruction,
)


def _execute_instruction(instruction, processor) -> None:
    hardware = Hardware(processor)
    instruction.execute(hardware)


@pytest.mark.parametrize("instruction", ALL_THREE_VALUE_INSTRUCTIONS)
def test_three_value_instructions_increment_pc_by_one(instruction):
    processor = Processor(program_counter=123)
    instruction_args = (1, 2, 3)
    _execute_instruction(instruction(*instruction_args), processor)
    assert processor.program_counter == 124


def test_add_registers_adds_the_values_of_two_registers():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = AddRegisters(register_out=0, register_a=1, register_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 19, 1: 12, 2: 7}


def test_add_immediate_adds_the_value_of_a_register_and_an_immediate():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = AddImmediate(register_out=0, register_a=1, value_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 14, 1: 12, 2: 7}


def test_multiply_registers_multiplies_the_values_of_two_registers():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = MultiplyRegisters(register_out=0, register_a=1, register_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 84, 1: 12, 2: 7}


def test_multiply_immediate_multiplies_the_value_of_a_register_and_an_immediate():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = MultiplyImmediate(register_out=0, register_a=1, value_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 24, 1: 12, 2: 7}


def test_bitwise_and_registers_performs_a_bitwise_and_on_the_values_of_two_registers():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = BitwiseAndRegisters(register_out=0, register_a=1, register_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 4, 1: 12, 2: 7}


def test_bitwise_and_immediate_performs_a_bitwise_and_on_the_value_of_a_register_and_an_immediate():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = BitwiseAndImmediate(register_out=0, register_a=1, value_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 0, 1: 12, 2: 7}


def test_bitwise_or_registers_performs_a_bitwise_or_on_the_values_of_two_registers():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = BitwiseOrRegisters(register_out=0, register_a=1, register_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 15, 1: 12, 2: 7}


def test_bitwise_or_immediate_performs_a_bitwise_or_on_the_value_of_a_register_and_an_immediate():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = BitwiseOrImmediate(register_out=0, register_a=1, value_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 14, 1: 12, 2: 7}


def test_assignment_registers_assigns_the_value_of_a_register_to_another_register():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = AssignmentRegisters(register_out=0, throwaway_value=0, register_in=1)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 12, 1: 12, 2: 7}


def test_assignment_immediate_assigns_the_value_of_an_immediate_to_a_register():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = AssignmentImmediate(register_out=0, throwaway_value=2, value_in=1)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 1, 1: 12, 2: 7}


def test_greater_than_immediate_register_sets_a_register_to_1_if_the_immediate_is_greater_than_the_register():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = GreaterThanImmediateRegister(register_out=0, value_a=8, register_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 1, 1: 12, 2: 7}


def test_greater_than_immediate_register_sets_a_register_to_0_if_the_immediate_is_not_greater_than_the_register():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = GreaterThanImmediateRegister(register_out=0, value_a=6, register_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 0, 1: 12, 2: 7}


def test_greater_than_register_immediate_sets_a_register_to_1_if_the_register_is_greater_than_the_immediate():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = GreaterThanRegisterImmediate(register_out=0, register_a=1, value_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 1, 1: 12, 2: 7}


def test_greater_than_register_immediate_sets_a_register_to_0_if_the_register_is_not_greater_than_the_immediate():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = GreaterThanRegisterImmediate(register_out=0, register_a=1, value_b=13)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 0, 1: 12, 2: 7}


def test_greater_than_register_register_sets_a_register_to_1_if_the_first_register_is_greater_than_the_second_register():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = GreaterThanRegisterRegister(
        register_out=0, register_a=1, register_b=2
    )
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 1, 1: 12, 2: 7}


def test_greater_than_register_register_sets_a_register_to_0_if_the_first_register_is_not_greater_than_the_second_register():
    processor = Processor(registers={0: 123, 1: 12, 2: 12})
    instruction = GreaterThanRegisterRegister(
        register_out=0, register_a=1, register_b=2
    )
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 0, 1: 12, 2: 12}


def test_equal_immediate_register_sets_a_register_to_1_if_the_immediate_is_equal_to_the_register():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = EqualImmediateRegister(register_out=0, value_a=7, register_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 1, 1: 12, 2: 7}


def test_equal_immediate_register_sets_a_register_to_0_if_the_immediate_is_not_equal_to_the_register():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = EqualImmediateRegister(register_out=0, value_a=1, register_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 0, 1: 12, 2: 7}


def test_equal_register_immediate_sets_a_register_to_1_if_the_register_is_equal_to_the_immediate():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = EqualRegisterImmediate(register_out=0, register_a=1, value_b=12)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 1, 1: 12, 2: 7}


def test_equal_register_immediate_sets_a_register_to_0_if_the_register_is_not_equal_to_the_immediate():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = EqualRegisterImmediate(register_out=0, register_a=1, value_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 0, 1: 12, 2: 7}


def test_equal_register_register_sets_a_register_to_1_if_the_first_register_is_equal_to_the_second_register():
    processor = Processor(registers={0: 123, 1: 12, 2: 12})
    instruction = EqualRegisterRegister(register_out=0, register_a=1, register_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 1, 1: 12, 2: 12}


def test_equal_register_register_sets_a_register_to_0_if_the_first_register_is_not_equal_to_the_second_register():
    processor = Processor(registers={0: 123, 1: 12, 2: 7})
    instruction = EqualRegisterRegister(register_out=0, register_a=1, register_b=2)
    _execute_instruction(instruction, processor)
    assert processor.registers == {0: 0, 1: 12, 2: 7}


@pytest.mark.parametrize("instruction", ALL_THREE_VALUE_INSTRUCTIONS)
def test_can_bind_program_counter_to_register_which_loads_pc_value_at_begining_of_instruction(
    instruction,
):
    processor = Processor(program_counter=123)
    instruction_args = (1, 2, 3)
    _execute_instruction(
        instruction(*instruction_args, register_bound_to_pc=7), processor
    )
    assert processor.registers[7] == 123


def test_can_bind_program_counter_to_register_which_overwrites_pc_at_end_of_instruction():
    value_1 = 321
    value_2 = 1_000
    program_counter = 7
    processor = Processor(
        program_counter=program_counter, registers={1: value_1, 2: value_2}
    )
    instruction = AddRegisters(
        register_a=1, register_b=2, register_out=1, register_bound_to_pc=1
    )
    expected_result = value_2 + program_counter

    _execute_instruction(instruction, processor)
    assert processor.registers[1] == expected_result
    assert processor.program_counter == expected_result + 1
