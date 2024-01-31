from models.assembly import Hardware, Processor
from models.aoc_2018.a2018_d16 import (
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
    possible_instructions,
    InstructionSample,
)


def _execute_instruction(instruction, processor) -> None:
    hardware = Hardware(processor)
    instruction.execute(hardware)


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
