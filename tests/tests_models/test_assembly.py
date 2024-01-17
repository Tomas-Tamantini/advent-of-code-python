from models.assembly import Computer, Processor, Program, Hardware
from unittest.mock import Mock


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
            hardware.processor.program_counter += 1

    class OutputInstruction:
        def execute(self, hardware):
            hardware.serial_output.write(hardware.processor.registers["a"])
            if hardware.processor.get_value("a") >= 9:
                hardware.processor.program_counter += 1
            else:
                hardware.processor.program_counter -= 1

    class MockProgram:
        def __init__(self):
            self.instructions = [IncrementInstruction(), OutputInstruction()]

        def get_instruction(self, program_counter):
            return self.instructions[program_counter] if program_counter < 2 else None

    processor = Processor(registers={"a": 1, "b": 2})
    serial_output = SerialOutputSpy()
    computer = Computer(
        hardware=Hardware(processor=processor, serial_output=serial_output)
    )
    computer.run_program(MockProgram())
    assert computer.get_register_value("a") == 9
    assert serial_output.output == [3, 5, 7, 9]
