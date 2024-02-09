from models.assembly import Hardware, Processor
from models.aoc_2019.intcode import (
    parse_next_instruction,
    IntcodeProgram,
    MemoryOrImmediate,
    IntcodeHalt,
    IntcodeAdd,
    IntcodeMultiply,
)


class _MockMemory:
    def __init__(self, memory):
        self.memory = memory

    def read(self, address):
        return self.memory[address]

    def write(self, address, value):
        self.memory[address] = value


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
