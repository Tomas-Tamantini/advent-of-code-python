from unittest.mock import Mock

from models.common.assembly import (
    AddInstruction,
    CopyInstruction,
    Hardware,
    InputInstruction,
    JumpGreaterThanZeroInstruction,
    OutInstruction,
    Processor,
)

from ..duet_code import (
    MultiplyInstruction,
    RecoverLastFrequencyInstruction,
    RemainderInstruction,
    last_recovered_frequency,
    sent_values_in_two_way_communication,
)


def test_recover_last_frequency_instruction_just_increments_pc_if_value_is_zero():
    audio_output_spy = Mock()
    processor = Processor({"a": 0}, program_counter=123)
    instruction = RecoverLastFrequencyInstruction("a")
    instruction.execute(
        hardware=Hardware(
            processor=processor,
            serial_output=audio_output_spy,
        )
    )
    assert processor.program_counter == 124
    audio_output_spy.write.assert_not_called()


def test_recover_last_frequency_increments_pc_and_sends_minus_one_to_output_if_register_is_not_zero():
    audio_output_spy = Mock()
    processor = Processor({"a": 1}, program_counter=123)
    instruction = RecoverLastFrequencyInstruction("a")
    instruction.execute(
        hardware=Hardware(
            processor=processor,
            serial_output=audio_output_spy,
        )
    )
    assert processor.program_counter == 124
    audio_output_spy.write.assert_called_once_with(-1)


def test_remainder_instruction_updates_source_with_source_mod_destination():
    processor = Processor({"a": 10, "b": 13}, program_counter=123)
    instruction = RemainderInstruction(source="a", destination="b")
    instruction.execute(hardware=Hardware(processor))
    assert processor.program_counter == 124
    assert processor.get_value_or_immediate("b") == 3


def test_multiply_instruction_updates_destination_with_source_times_destination():
    processor = Processor({"a": 10, "b": 13}, program_counter=123)
    instruction = MultiplyInstruction(source="a", destination="b")
    instruction.execute(hardware=Hardware(processor))
    assert processor.program_counter == 124
    assert processor.get_value_or_immediate("a") == 10
    assert processor.get_value_or_immediate("b") == 130


def test_program_keeps_track_of_last_recovered_frequency():
    instructions = [
        CopyInstruction(source=1, destination="a"),
        AddInstruction(source=2, destination="a"),
        MultiplyInstruction(source="a", destination="a"),
        RemainderInstruction(source=5, destination="a"),
        OutInstruction(source="a"),
        CopyInstruction(source=0, destination="a"),
        RecoverLastFrequencyInstruction(source="a"),
        JumpGreaterThanZeroInstruction(offset=-1, value_to_compare="a"),
        CopyInstruction(source=1, destination="a"),
        JumpGreaterThanZeroInstruction(offset=-2, value_to_compare="a"),
    ]
    assert last_recovered_frequency(instructions) == 4


def test_computers_keep_track_of_values_they_send():
    instructions = [
        OutInstruction(1),
        OutInstruction(2),
        OutInstruction("p"),
        InputInstruction("a"),
        InputInstruction("b"),
        InputInstruction("c"),
        InputInstruction("d"),
    ]
    assert sent_values_in_two_way_communication(instructions) == {
        "0": [1, 2, 0],
        "1": [1, 2, 1],
    }
