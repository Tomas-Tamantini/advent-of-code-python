import pytest

from models.common.assembly import Hardware, Processor, SerialInput, SerialOutput

from .instruction_parser import parse_next_instruction
from .instructions import (
    IntcodeAdd,
    IntcodeEquals,
    IntcodeHalt,
    IntcodeInput,
    IntcodeJumpIfFalse,
    IntcodeJumpIfTrue,
    IntcodeLessThan,
    IntcodeMultiply,
    IntcodeOutput,
    IntcodeParameter,
    IntcodeRelativeBaseOffset,
    ParameterMode,
)
from .program import IntcodeProgram
from .run_program import run_intcode_program


class _MockMemory:
    def __init__(self, memory):
        self.memory = memory

    def read(self, address):
        return self.memory[address]

    def write(self, address, value):
        self.memory[address] = value


class _MockSerialInput:
    def __init__(self, input_value: int = 123) -> None:
        self._input_value = input_value

    def read(self):
        return self._input_value


class _MockSerialOutput:
    def __init__(self) -> None:
        self.output_values = []

    def write(self, value: int) -> None:
        self.output_values.append(value)


def test_intcode_parameter_returns_value_from_immediate():
    immediate = IntcodeParameter(3, parameter_mode=ParameterMode.IMMEDIATE)
    hardware = _build_hardware([10, 20, 30, 40, 50])
    assert immediate.get_value(hardware) == 3


def test_intcode_parameter_returns_value_from_position():
    immediate = IntcodeParameter(3, parameter_mode=ParameterMode.POSITION)
    hardware = _build_hardware([10, 20, 30, 40, 50])
    assert immediate.get_value(hardware) == 40


def test_intcode_parameter_returns_value_from_position_with_relative_base():
    immediate = IntcodeParameter(3, parameter_mode=ParameterMode.RELATIVE)
    hardware = _build_hardware([10, 20, 30, 40, 50], relative_base=-2)
    assert immediate.get_value(hardware) == 20


def _build_hardware(
    memory_values: list[int] = None,
    serial_input: SerialInput = None,
    serial_output: SerialOutput = None,
    program_counter: int = 0,
    relative_base=0,
):
    if memory_values is None:
        memory_values = [0] * 10
    if serial_input is None:
        serial_input = _MockSerialInput()
    if serial_output is None:
        serial_output = _MockSerialOutput()
    return Hardware(
        processor=Processor(program_counter=program_counter),
        memory=_MockMemory(memory=memory_values),
        serial_input=serial_input,
        serial_output=serial_output,
        relative_base=relative_base,
    )


def test_intcode_add_writes_sum_of_inputs_to_output_address():
    add = IntcodeAdd(
        input_a=IntcodeParameter(1, parameter_mode=ParameterMode.POSITION),
        input_b=IntcodeParameter(2, parameter_mode=ParameterMode.POSITION),
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    add.execute(hardware)
    assert hardware.memory.read(address=3) == 50


def test_intcode_add_increments_pc_by_four():
    add = IntcodeAdd(
        input_a=IntcodeParameter(1, parameter_mode=ParameterMode.IMMEDIATE),
        input_b=IntcodeParameter(2, parameter_mode=ParameterMode.IMMEDIATE),
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware(program_counter=17)
    add.execute(hardware)
    assert hardware.processor.program_counter == 21


def test_intcode_multiply_writes_product_of_inputs_to_output_address():
    multiply = IntcodeMultiply(
        input_a=IntcodeParameter(1, parameter_mode=ParameterMode.POSITION),
        input_b=IntcodeParameter(2, parameter_mode=ParameterMode.POSITION),
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    multiply.execute(hardware)
    assert hardware.memory.read(address=3) == 600


def test_intcode_multiply_increments_pc_by_four():
    multiply = IntcodeMultiply(
        input_a=IntcodeParameter(1, parameter_mode=ParameterMode.IMMEDIATE),
        input_b=IntcodeParameter(2, parameter_mode=ParameterMode.IMMEDIATE),
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware(program_counter=17)
    multiply.execute(hardware)
    assert hardware.processor.program_counter == 21


def test_intcode_halt_sets_pc_to_negative_one_to_halt():
    halt = IntcodeHalt()
    hardware = _build_hardware()
    halt.execute(hardware)
    assert hardware.processor.program_counter == -1


def test_intcode_input_reads_from_serial_input_and_writes_to_memory():
    input_instruction = IntcodeInput(
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION)
    )
    hardware = Hardware(
        processor=Processor(),
        memory=_MockMemory([0] * 10),
        serial_input=_MockSerialInput(123),
    )
    input_instruction.execute(hardware)
    assert hardware.memory.read(address=3) == 123


def test_intcode_input_increments_pc_by_two():
    input_instruction = IntcodeInput(
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION)
    )
    hardware = _build_hardware(program_counter=17)
    input_instruction.execute(hardware)
    assert hardware.processor.program_counter == 19


def test_intcode_output_reads_from_memory_and_writes_to_serial_output():
    output_instruction = IntcodeOutput(
        value=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION)
    )
    hardware = Hardware(
        processor=Processor(),
        memory=_MockMemory([0, 0, 0, 123]),
        serial_output=_MockSerialOutput(),
    )
    output_instruction.execute(hardware)
    assert hardware.serial_output.output_values[-1] == 123


def test_intcode_output_increments_pc_by_two():
    output_instruction = IntcodeOutput(
        value=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION)
    )
    hardware = _build_hardware(program_counter=17)
    output_instruction.execute(hardware)
    assert hardware.processor.program_counter == 19


def test_intcode_jump_if_true_jumps_if_input_is_nonzero():
    instruction = IntcodeJumpIfTrue(
        condition=IntcodeParameter(1, parameter_mode=ParameterMode.POSITION),
        jump_address=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50], program_counter=123)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 40


def test_intcode_jump_if_true_does_not_jump_if_input_is_zero():
    instruction = IntcodeJumpIfTrue(
        condition=IntcodeParameter(0, parameter_mode=ParameterMode.IMMEDIATE),
        jump_address=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50], program_counter=123)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 126


def test_intcode_jump_if_false_jumps_if_input_is_zero():
    instruction = IntcodeJumpIfFalse(
        condition=IntcodeParameter(1, parameter_mode=ParameterMode.POSITION),
        jump_address=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 0, 30, 40, 50], program_counter=123)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 40


def test_intcode_jump_if_false_does_not_jump_if_input_is_nonzero():
    instruction = IntcodeJumpIfFalse(
        condition=IntcodeParameter(1, parameter_mode=ParameterMode.IMMEDIATE),
        jump_address=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50], program_counter=123)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 126


def test_intcode_less_than_writes_one_to_output_if_input_a_is_less_than_input_b():
    instruction = IntcodeLessThan(
        input_a=IntcodeParameter(1, parameter_mode=ParameterMode.POSITION),
        input_b=IntcodeParameter(2, parameter_mode=ParameterMode.POSITION),
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    instruction.execute(hardware)
    assert hardware.memory.read(address=3) == 1


def test_intcode_less_than_writes_zero_to_output_if_input_a_is_not_less_than_input_b():
    instruction = IntcodeLessThan(
        input_a=IntcodeParameter(2, parameter_mode=ParameterMode.POSITION),
        input_b=IntcodeParameter(1, parameter_mode=ParameterMode.POSITION),
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    instruction.execute(hardware)
    assert hardware.memory.read(address=3) == 0


def test_intcode_less_than_increments_pc_by_four():
    instruction = IntcodeLessThan(
        input_a=IntcodeParameter(1, parameter_mode=ParameterMode.POSITION),
        input_b=IntcodeParameter(2, parameter_mode=ParameterMode.POSITION),
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware(program_counter=17)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 21


def test_intcode_equals_writes_one_to_output_if_input_a_equals_input_b():
    instruction = IntcodeEquals(
        input_a=IntcodeParameter(30, parameter_mode=ParameterMode.IMMEDIATE),
        input_b=IntcodeParameter(2, parameter_mode=ParameterMode.POSITION),
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    instruction.execute(hardware)
    assert hardware.memory.read(address=3) == 1


def test_intcode_equals_writes_zero_to_output_if_input_a_does_not_equal_input_b():
    instruction = IntcodeEquals(
        input_a=IntcodeParameter(1, parameter_mode=ParameterMode.POSITION),
        input_b=IntcodeParameter(2, parameter_mode=ParameterMode.POSITION),
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    instruction.execute(hardware)
    assert hardware.memory.read(address=3) == 0


def test_intcode_equals_increments_pc_by_four():
    instruction = IntcodeEquals(
        input_a=IntcodeParameter(1, parameter_mode=ParameterMode.POSITION),
        input_b=IntcodeParameter(2, parameter_mode=ParameterMode.POSITION),
        output=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware(program_counter=17)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 21


def test_intcode_relative_base_offset_increments_relative_base_by_input_value():
    instruction = IntcodeRelativeBaseOffset(
        offset=IntcodeParameter(3, parameter_mode=ParameterMode.POSITION),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50], relative_base=7)
    instruction.execute(hardware)
    assert hardware.relative_base == 47


def test_parameters_can_be_in_position_or_immediate_or_relative_mode():
    instruction = parse_next_instruction([21002, 4, 3, 4])
    assert isinstance(instruction, IntcodeMultiply)
    assert instruction.input_a.value == 4
    assert instruction.input_a.parameter_mode == ParameterMode.POSITION
    assert instruction.input_b.value == 3
    assert instruction.input_b.parameter_mode == ParameterMode.IMMEDIATE
    assert instruction.output.value == 4
    assert instruction.output.parameter_mode == ParameterMode.RELATIVE


def test_op_code_99_parses_to_halt_instruction():
    instruction = parse_next_instruction([99, 1, 2, 3])
    assert isinstance(instruction, IntcodeHalt)


def test_op_code_1_parses_to_add_instruction():
    instruction = parse_next_instruction([1, 1, 2, 3])
    assert isinstance(instruction, IntcodeAdd)
    assert instruction.input_a.value == 1
    assert instruction.input_a.parameter_mode == ParameterMode.POSITION
    assert instruction.input_b.value == 2
    assert instruction.input_b.parameter_mode == ParameterMode.POSITION
    assert instruction.output.value == 3
    assert instruction.output.parameter_mode == ParameterMode.POSITION


def test_op_code_2_parses_to_multiply_instruction():
    instruction = parse_next_instruction([2, 1, 2, 3])
    assert isinstance(instruction, IntcodeMultiply)
    assert instruction.input_a.value == 1
    assert instruction.input_a.parameter_mode == ParameterMode.POSITION
    assert instruction.input_b.value == 2
    assert instruction.input_b.parameter_mode == ParameterMode.POSITION
    assert instruction.output.value == 3
    assert instruction.output.parameter_mode == ParameterMode.POSITION


def test_op_code_3_parses_to_input_instruction():
    instruction = parse_next_instruction([3, 1])
    assert isinstance(instruction, IntcodeInput)
    assert instruction.output.value == 1
    assert instruction.output.parameter_mode == ParameterMode.POSITION


def test_op_code_4_parses_to_output_instruction():
    instruction = parse_next_instruction([4, 1])
    assert isinstance(instruction, IntcodeOutput)
    assert instruction.value.value == 1
    assert instruction.value.parameter_mode == ParameterMode.POSITION


def test_op_code_5_parses_to_jump_if_true_instruction():
    instruction = parse_next_instruction([5, 1, 2])
    assert isinstance(instruction, IntcodeJumpIfTrue)
    assert instruction.condition.value == 1
    assert instruction.condition.parameter_mode == ParameterMode.POSITION
    assert instruction.jump_address.value == 2
    assert instruction.jump_address.parameter_mode == ParameterMode.POSITION


def test_op_code_6_parses_to_jump_if_false_instruction():
    instruction = parse_next_instruction([6, 1, 2])
    assert isinstance(instruction, IntcodeJumpIfFalse)
    assert instruction.condition.value == 1
    assert instruction.condition.parameter_mode == ParameterMode.POSITION
    assert instruction.jump_address.value == 2
    assert instruction.jump_address.parameter_mode == ParameterMode.POSITION


def test_op_code_7_parses_to_less_than_instruction():
    instruction = parse_next_instruction([7, 1, 2, 3])
    assert isinstance(instruction, IntcodeLessThan)
    assert instruction.input_a.value == 1
    assert instruction.input_a.parameter_mode == ParameterMode.POSITION
    assert instruction.input_b.value == 2
    assert instruction.input_b.parameter_mode == ParameterMode.POSITION
    assert instruction.output.value == 3
    assert instruction.output.parameter_mode == ParameterMode.POSITION


def test_op_code_8_parses_to_equals_instruction():
    instruction = parse_next_instruction([8, 1, 2, 3])
    assert isinstance(instruction, IntcodeEquals)
    assert instruction.input_a.value == 1
    assert instruction.input_a.parameter_mode == ParameterMode.POSITION
    assert instruction.input_b.value == 2
    assert instruction.input_b.parameter_mode == ParameterMode.POSITION
    assert instruction.output.value == 3
    assert instruction.output.parameter_mode == ParameterMode.POSITION


def test_op_code_9_parses_to_relative_base_offset_instruction():
    instruction = parse_next_instruction([9, 3])
    assert isinstance(instruction, IntcodeRelativeBaseOffset)
    assert instruction.offset.value == 3
    assert instruction.offset.parameter_mode == ParameterMode.POSITION


def test_intcode_program_get_instruction_returns_instruction_at_pc():
    program = IntcodeProgram(instructions=[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    instruction = program.get_instruction(program_counter=0)
    assert isinstance(instruction, IntcodeAdd)
    assert instruction.input_a.value == 9
    assert instruction.input_a.parameter_mode == ParameterMode.POSITION
    assert instruction.input_b.value == 10
    assert instruction.input_b.parameter_mode == ParameterMode.POSITION
    assert instruction.output.value == 3
    assert instruction.output.parameter_mode == ParameterMode.POSITION
    instruction = program.get_instruction(program_counter=4)
    assert isinstance(instruction, IntcodeMultiply)
    assert instruction.input_a.value == 3
    assert instruction.input_a.parameter_mode == ParameterMode.POSITION
    assert instruction.input_b.value == 11
    assert instruction.input_b.parameter_mode == ParameterMode.POSITION
    assert instruction.output.value == 0
    assert instruction.output.parameter_mode == ParameterMode.POSITION
    instruction = program.get_instruction(program_counter=8)
    assert isinstance(instruction, IntcodeHalt)


def test_reading_instruction_at_negative_value_from_intcode_program_returns_none():
    program = IntcodeProgram(instructions=[99])
    assert program.get_instruction(program_counter=-1) is None


def test_intcode_program_allows_reading_and_writing_values():
    program = IntcodeProgram(instructions=[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    assert program.read(address=6) == 11
    program.write(address=6, new_value=100)
    assert program.read(address=6) == 100


def test_reading_and_writing_intcode_program_values_with_negative_address_raises_index_error():
    program = IntcodeProgram(instructions=[99])
    with pytest.raises(IndexError):
        program.read(address=-1)
    with pytest.raises(IndexError):
        program.write(address=-1, new_value=100)


def test_reading_intcode_program_value_above_max_address_returns_zero():
    program = IntcodeProgram(instructions=[99])
    assert program.read(address=100) == 0


def test_writing_intcode_program_can_be_done_at_any_positive_address():
    program = IntcodeProgram(instructions=[99])
    program.write(address=1_000_000, new_value=123)
    assert program.read(address=1_000_000) == 123


def test_running_intcode_program_runs_it_until_halt():
    program = IntcodeProgram(instructions=[1001, 0, 100, 2, 99])
    run_intcode_program(program)
    assert list(program.contiguous_instructions) == [1001, 0, 1101, 2, 99]


@pytest.mark.parametrize(
    ("instructions", "expected_output"),
    [
        ([1102, 34915192, 34915192, 7, 4, 7, 99, 0], 1219070632396864),
        ([104, 1125899906842624, 99], 1125899906842624),
    ],
)
def test_intcode_program_can_handle_large_integers(instructions, expected_output):
    output = _MockSerialOutput()
    program = IntcodeProgram(instructions)
    run_intcode_program(program, serial_output=output)
    assert output.output_values[-1] == expected_output


def test_test_intcode_program_has_quine():
    quine = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    output = _MockSerialOutput()
    program = IntcodeProgram(instructions=quine)
    run_intcode_program(program, serial_output=output)
    assert output.output_values == quine
