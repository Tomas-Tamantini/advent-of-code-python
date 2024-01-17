import pytest
from unittest.mock import Mock
from models.assembly import Computer, Processor, Program, Hardware, ImmutableProgram


def test_computer_can_be_initialized_from_processor():
    processor = Processor(registers={"a": 1, "b": 2})
    computer = Computer.from_processor(processor)
    assert computer.get_register_value("a") == 1
    assert computer.get_register_value("b") == 2


def test_running_program_with_no_instructions_does_nothing():
    processor = Processor(registers={"a": 1, "b": 2})
    computer = Computer.from_processor(processor)
    empty_program = Mock(spec=Program)
    empty_program.get_instruction.return_value = None
    computer.run_program(empty_program)
    assert computer.get_register_value("a") == 1
    assert computer.get_register_value("b") == 2


def test_program_instructions_are_executed_until_end_of_program():
    class SerialOutputSpy:
        def __init__(self):
            self.output = []

        def write(self, value):
            self.output.append(value)

    class IncrementInstruction:
        def execute(self, hardware):
            hardware.processor.registers["a"] += hardware.processor.get_value("b")
            hardware.increment_program_counter()

    class OutputInstruction:
        def execute(self, hardware):
            hardware.serial_output.write(hardware.processor.registers["a"])
            if hardware.processor.get_value("a") >= 9:
                hardware.increment_program_counter()
            else:
                hardware.increment_program_counter(increment=-1)

    program = ImmutableProgram([IncrementInstruction(), OutputInstruction()])

    processor = Processor(registers={"a": 1, "b": 2})
    serial_output = SerialOutputSpy()
    computer = Computer(
        hardware=Hardware(processor=processor, serial_output=serial_output)
    )
    computer.run_program(program)
    assert computer.get_register_value("a") == 9
    assert serial_output.output == [3, 5, 7, 9]


def test_can_execute_instructions_one_by_one():
    class NoOpInstruction:
        def execute(self, hardware):
            hardware.increment_program_counter()

    program = ImmutableProgram([NoOpInstruction(), NoOpInstruction()])
    processor = Processor()
    computer = Computer.from_processor(processor)
    computer.run_next_instruction(program)
    assert computer._program_counter == 1
    computer.run_next_instruction(program)
    assert computer._program_counter == 2
    with pytest.raises(StopIteration):
        computer.run_next_instruction(program)
