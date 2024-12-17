from unittest.mock import Mock

import pytest

from models.common.assembly import Hardware, Processor, SerialOutput

from ..logic.instructions_3_bit import (
    Division3BitInstruction,
    JumpNotZero3BitInstruction,
    Modulo3BitInstruction,
    Output3BitInstruction,
    XorLiteral3BitInstruction,
    XorRegisters3BitInstruction,
)


@pytest.mark.parametrize(
    "instruction",
    [
        Division3BitInstruction("A", "B", 3),
        XorLiteral3BitInstruction("A", 3),
        XorRegisters3BitInstruction("A", "B"),
        Modulo3BitInstruction("A", 3, 5),
        Output3BitInstruction(5, 8),
    ],
)
def test_non_jump_3_bit_instruction_increments_pc_by_two(instruction):
    hardware = Hardware(Processor(program_counter=11), serial_output=Mock())
    instruction.execute(hardware)
    assert 13 == hardware.processor.program_counter


def test_division_3_bit_instruction_writes_result_of_division_in_output_register():
    instruction = Division3BitInstruction(
        numerator_register="A", output_register="B", operand=2
    )
    hardware = Hardware(Processor(registers={"A": 45, "B": 0}))
    expected_result = 11  # 45 // (2^2)
    instruction.execute(hardware)
    assert expected_result == hardware.get_value_at_register("B")


def test_division_3_bit_instruction_uses_combo_operand():
    instruction = Division3BitInstruction(
        numerator_register="A", output_register="B", operand=5
    )
    hardware = Hardware(Processor(registers={"A": 45, "B": 3}))
    expected_result = 5  # 45 // (2^B)
    instruction.execute(hardware)
    assert expected_result == hardware.get_value_at_register("B")


def test_xor_literal_3_bit_instruction_writes_result_in_same_input_register():
    instruction = XorLiteral3BitInstruction(register="A", literal=0b110)
    hardware = Hardware(Processor(registers={"A": 0b1010}))
    expected_result = 0b1100
    instruction.execute(hardware)
    assert expected_result == hardware.get_value_at_register("A")


def test_xor_registers_3_bit_instruction_writes_result_in_first_input_register():
    instruction = XorRegisters3BitInstruction(register_a="A", register_b="B")
    hardware = Hardware(Processor(registers={"A": 0b1010, "B": 0b1100}))
    expected_result = 0b0110
    instruction.execute(hardware)
    assert expected_result == hardware.get_value_at_register("A")


def test_modulo_3_bit_instruction_writes_result_of_modulo_in_output_register():
    instruction = Modulo3BitInstruction(output_register="A", operand=3, modulo=2)
    hardware = Hardware(processor=Processor(registers={"A": 0}))
    expected_result = 1  # 3 % 2
    instruction.execute(hardware)
    assert expected_result == hardware.get_value_at_register("A")


def test_modulo_3_bit_instruction_uses_combo_operator():
    instruction = Modulo3BitInstruction(output_register="A", operand=6, modulo=8)
    hardware = Hardware(processor=Processor(registers={"A": 0, "C": 1357}))
    expected_result = 5  # C % 8
    instruction.execute(hardware)
    assert expected_result == hardware.get_value_at_register("A")


def test_jump_not_zero_3_bit_instruction_increments_pc_by_two_if_register_is_zero():
    instruction = JumpNotZero3BitInstruction(register="A", new_pc=0)
    hardware = Hardware(Processor(program_counter=11, registers={"A": 0}))
    instruction.execute(hardware)
    assert 13 == hardware.processor.program_counter


def test_jump_not_zero_3_bit_instruction_jumps_to_new_pc_if_register_is_not_zero():
    instruction = JumpNotZero3BitInstruction(register="A", new_pc=123)
    hardware = Hardware(Processor(program_counter=11, registers={"A": 1}))
    instruction.execute(hardware)
    assert 123 == hardware.processor.program_counter


def test_output_3_bit_instruction_outputs_operand_mod_to_serial_output():
    instruction = Output3BitInstruction(operand=3, modulo=2)
    serial_output = Mock(spec=SerialOutput)
    hardware = Hardware(Processor(), serial_output=serial_output)
    instruction.execute(hardware)
    serial_output.write.assert_called_once_with(1)  # 3 % 2


def test_output_3_bit_instruction_uses_combo_operand():
    instruction = Output3BitInstruction(operand=6, modulo=8)
    serial_output = Mock(spec=SerialOutput)
    hardware = Hardware(Processor(registers={"C": 1357}), serial_output=serial_output)
    instruction.execute(hardware)
    serial_output.write.assert_called_once_with(5)  # 1357 % 8
