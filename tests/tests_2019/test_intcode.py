from models.assembly import Hardware, Processor
from models.aoc_2019.intcode import (
    parse_next_instruction,
    IntcodeProgram,
    MemoryOrImmediate,
    IntcodeHalt,
    IntcodeAdd,
    IntcodeMultiply,
    IntcodeInput,
    IntcodeOutput,
    IntcodeJumpIfTrue,
    IntcodeJumpIfFalse,
    IntcodeLessThan,
    IntcodeEquals,
)


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
        self.output_value = None

    def write(self, value: int) -> None:
        self.output_value = value


def test_memory_or_immediate_get_value_returns_memory_value_or_immediate():
    immediate = MemoryOrImmediate(3, is_memory=False)
    memory = MemoryOrImmediate(3, is_memory=True)
    hardware = _build_hardware([10, 20, 30, 40, 50])
    assert immediate.get_value(hardware) == 3
    assert memory.get_value(hardware) == 40


def _build_hardware(memory_values: list[int] = None, program_counter: int = 0):
    if memory_values is None:
        memory_values = [0] * 10
    return Hardware(
        processor=Processor(program_counter=program_counter),
        memory=_MockMemory(memory=memory_values),
        serial_input=_MockSerialInput(),
        serial_output=_MockSerialOutput(),
    )


def test_intcode_add_writes_sum_of_inputs_to_output_address():
    add = IntcodeAdd(
        input_a=MemoryOrImmediate(1, is_memory=True),
        input_b=MemoryOrImmediate(2, is_memory=True),
        output=3,
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    add.execute(hardware)
    assert hardware.memory.read(address=3) == 50


def test_intcode_add_increments_pc_by_four():
    add = IntcodeAdd(
        input_a=MemoryOrImmediate(1, is_memory=False),
        input_b=MemoryOrImmediate(2, is_memory=False),
        output=3,
    )
    hardware = _build_hardware(program_counter=17)
    add.execute(hardware)
    assert hardware.processor.program_counter == 21


def test_intcode_multiply_writes_product_of_inputs_to_output_address():
    multiply = IntcodeMultiply(
        input_a=MemoryOrImmediate(1, is_memory=True),
        input_b=MemoryOrImmediate(2, is_memory=True),
        output=3,
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    multiply.execute(hardware)
    assert hardware.memory.read(address=3) == 600


def test_intcode_multiply_increments_pc_by_four():
    multiply = IntcodeMultiply(
        input_a=MemoryOrImmediate(1, is_memory=False),
        input_b=MemoryOrImmediate(2, is_memory=False),
        output=3,
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

    input_instruction = IntcodeInput(output=3)
    hardware = Hardware(
        processor=Processor(),
        memory=_MockMemory([0] * 10),
        serial_input=_MockSerialInput(123),
    )
    input_instruction.execute(hardware)
    assert hardware.memory.read(address=3) == 123


def test_intcode_input_increments_pc_by_two():
    input_instruction = IntcodeInput(output=3)
    hardware = _build_hardware(program_counter=17)
    input_instruction.execute(hardware)
    assert hardware.processor.program_counter == 19


def test_intcode_output_reads_from_memory_and_writes_to_serial_output():
    output_instruction = IntcodeOutput(value=MemoryOrImmediate(3, is_memory=True))
    hardware = Hardware(
        processor=Processor(),
        memory=_MockMemory([0, 0, 0, 123]),
        serial_output=_MockSerialOutput(),
    )
    output_instruction.execute(hardware)
    assert hardware.serial_output.output_value == 123


def test_intcode_output_increments_pc_by_two():
    output_instruction = IntcodeOutput(value=MemoryOrImmediate(3, is_memory=True))
    hardware = _build_hardware(program_counter=17)
    output_instruction.execute(hardware)
    assert hardware.processor.program_counter == 19


def test_intcode_jump_if_true_jumps_if_input_is_nonzero():
    instruction = IntcodeJumpIfTrue(
        condition=MemoryOrImmediate(1, is_memory=True),
        jump_address=MemoryOrImmediate(3, is_memory=True),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50], program_counter=123)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 40


def test_intcode_jump_if_true_does_not_jump_if_input_is_zero():
    instruction = IntcodeJumpIfTrue(
        condition=MemoryOrImmediate(0, is_memory=False),
        jump_address=MemoryOrImmediate(3, is_memory=True),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50], program_counter=123)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 126


def test_intcode_jump_if_false_jumps_if_input_is_zero():
    instruction = IntcodeJumpIfFalse(
        condition=MemoryOrImmediate(1, is_memory=True),
        jump_address=MemoryOrImmediate(3, is_memory=True),
    )
    hardware = _build_hardware([10, 0, 30, 40, 50], program_counter=123)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 40


def test_intcode_jump_if_false_does_not_jump_if_input_is_nonzero():
    instruction = IntcodeJumpIfFalse(
        condition=MemoryOrImmediate(1, is_memory=False),
        jump_address=MemoryOrImmediate(3, is_memory=True),
    )
    hardware = _build_hardware([10, 20, 30, 40, 50], program_counter=123)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 126


def test_intcode_less_than_writes_one_to_output_if_input_a_is_less_than_input_b():
    instruction = IntcodeLessThan(
        input_a=MemoryOrImmediate(1, is_memory=True),
        input_b=MemoryOrImmediate(2, is_memory=True),
        output=3,
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    instruction.execute(hardware)
    assert hardware.memory.read(address=3) == 1


def test_intcode_less_than_writes_zero_to_output_if_input_a_is_not_less_than_input_b():
    instruction = IntcodeLessThan(
        input_a=MemoryOrImmediate(2, is_memory=True),
        input_b=MemoryOrImmediate(1, is_memory=True),
        output=3,
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    instruction.execute(hardware)
    assert hardware.memory.read(address=3) == 0


def test_intcode_less_than_increments_pc_by_four():
    instruction = IntcodeLessThan(
        input_a=MemoryOrImmediate(1, is_memory=True),
        input_b=MemoryOrImmediate(2, is_memory=True),
        output=3,
    )
    hardware = _build_hardware(program_counter=17)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 21


def test_intcode_equals_writes_one_to_output_if_input_a_equals_input_b():
    instruction = IntcodeEquals(
        input_a=MemoryOrImmediate(30, is_memory=False),
        input_b=MemoryOrImmediate(2, is_memory=True),
        output=3,
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    instruction.execute(hardware)
    assert hardware.memory.read(address=3) == 1


def test_intcode_equals_writes_zero_to_output_if_input_a_does_not_equal_input_b():
    instruction = IntcodeEquals(
        input_a=MemoryOrImmediate(1, is_memory=True),
        input_b=MemoryOrImmediate(2, is_memory=True),
        output=3,
    )
    hardware = _build_hardware([10, 20, 30, 40, 50])
    instruction.execute(hardware)
    assert hardware.memory.read(address=3) == 0


def test_intcode_equals_increments_pc_by_four():
    instruction = IntcodeEquals(
        input_a=MemoryOrImmediate(1, is_memory=True),
        input_b=MemoryOrImmediate(2, is_memory=True),
        output=3,
    )
    hardware = _build_hardware(program_counter=17)
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 21


def test_parameters_can_be_in_position_or_immediate_mode():
    instruction = parse_next_instruction([1002, 4, 3, 4])
    assert isinstance(instruction, IntcodeMultiply)
    assert instruction.input_a.value == 4
    assert instruction.input_a.is_memory
    assert instruction.input_b.value == 3
    assert not instruction.input_b.is_memory
    assert instruction.output == 4


def test_op_code_99_parses_to_halt_instruction():
    instruction = parse_next_instruction([99, 1, 2, 3])
    assert isinstance(instruction, IntcodeHalt)


def test_op_code_1_parses_to_add_instruction():
    instruction = parse_next_instruction([1, 1, 2, 3])
    assert isinstance(instruction, IntcodeAdd)
    assert instruction.input_a.value == 1
    assert instruction.input_a.is_memory
    assert instruction.input_b.value == 2
    assert instruction.input_b.is_memory
    assert instruction.output == 3


def test_op_code_2_parses_to_multiply_instruction():
    instruction = parse_next_instruction([2, 1, 2, 3])
    assert isinstance(instruction, IntcodeMultiply)
    assert instruction.input_a.value == 1
    assert instruction.input_a.is_memory
    assert instruction.input_b.value == 2
    assert instruction.input_b.is_memory
    assert instruction.output == 3


def test_op_code_3_parses_to_input_instruction():
    instruction = parse_next_instruction([3, 1])
    assert isinstance(instruction, IntcodeInput)
    assert instruction.output == 1


def test_op_code_4_parses_to_output_instruction():
    instruction = parse_next_instruction([4, 1])
    assert isinstance(instruction, IntcodeOutput)
    assert instruction.value.value == 1
    assert instruction.value.is_memory


def test_op_code_5_parses_to_jump_if_true_instruction():
    instruction = parse_next_instruction([5, 1, 2])
    assert isinstance(instruction, IntcodeJumpIfTrue)
    assert instruction.condition.value == 1
    assert instruction.condition.is_memory
    assert instruction.jump_address.value == 2
    assert instruction.jump_address.is_memory


def test_op_code_6_parses_to_jump_if_false_instruction():
    instruction = parse_next_instruction([6, 1, 2])
    assert isinstance(instruction, IntcodeJumpIfFalse)
    assert instruction.condition.value == 1
    assert instruction.condition.is_memory
    assert instruction.jump_address.value == 2
    assert instruction.jump_address.is_memory


def test_op_code_7_parses_to_less_than_instruction():
    instruction = parse_next_instruction([7, 1, 2, 3])
    assert isinstance(instruction, IntcodeLessThan)
    assert instruction.input_a.value == 1
    assert instruction.input_a.is_memory
    assert instruction.input_b.value == 2
    assert instruction.input_b.is_memory
    assert instruction.output == 3


def test_op_code_8_parses_to_equals_instruction():
    instruction = parse_next_instruction([8, 1, 2, 3])
    assert isinstance(instruction, IntcodeEquals)
    assert instruction.input_a.value == 1
    assert instruction.input_a.is_memory
    assert instruction.input_b.value == 2
    assert instruction.input_b.is_memory
    assert instruction.output == 3


def test_intcode_program_get_instruction_returns_instruction_at_pc():
    program = IntcodeProgram(sequence=[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    instruction = program.get_instruction(program_counter=0)
    assert isinstance(instruction, IntcodeAdd)
    assert instruction.input_a.value == 9
    assert instruction.input_a.is_memory
    assert instruction.input_b.value == 10
    assert instruction.input_b.is_memory
    assert instruction.output == 3
    instruction = program.get_instruction(program_counter=4)
    assert isinstance(instruction, IntcodeMultiply)
    assert instruction.input_a.value == 3
    assert instruction.input_a.is_memory
    assert instruction.input_b.value == 11
    assert instruction.input_b.is_memory
    assert instruction.output == 0
    instruction = program.get_instruction(program_counter=8)
    assert isinstance(instruction, IntcodeHalt)


def test_intcode_program_allows_reading_and_writing_values():
    program = IntcodeProgram(sequence=[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    assert program.read(address=6) == 11
    program.write(address=6, new_value=100)
    assert program.read(address=6) == 100