from unittest.mock import Mock

from models.common.assembly import (
    AddInstruction,
    CopyInstruction,
    Hardware,
    JumpNotZeroInstruction,
    Processor,
)

from .coprocessor import (
    InstructionCounter,
    SpyMultiplyInstruction,
    count_multiply_instructions,
)


def test_spy_instruction_updates_register_and_writes_to_serial_output():
    instruction = SpyMultiplyInstruction(source="a", destination="b")
    mock_serial_output = Mock()
    hardware = Hardware(
        processor=Processor(registers={"a": 5, "b": 4}),
        serial_output=mock_serial_output,
    )
    instruction.execute(hardware)
    assert hardware.processor.program_counter == 1
    assert hardware.get_value_at_register("a") == 5
    assert hardware.get_value_at_register("b") == 20
    mock_serial_output.write.assert_called_once_with(1)


def test_instruction_counter_counts_how_many_times_write_was_called():
    instruction_counter = InstructionCounter()
    instruction_counter.write(1)
    instruction_counter.write(1)
    assert instruction_counter.count == 2


def test_can_count_how_many_times_multiply_was_called():
    instructions = [
        CopyInstruction(source=3, destination="x"),
        SpyMultiplyInstruction(source="a", destination="b"),
        SpyMultiplyInstruction(source="b", destination="a"),
        AddInstruction(source=-1, destination="x"),
        JumpNotZeroInstruction(offset=-3, value_to_compare="x"),
    ]
    assert count_multiply_instructions(instructions) == 6
