import pytest
from models.aoc_2019.a2019_d21 import (
    SpringScriptInstruction,
    SpringScriptInstructionType,
    SpringDroidInput,
)


def test_springscript_instruction_can_be_converted_to_string():
    instruction = SpringScriptInstruction(SpringScriptInstructionType.AND, "A", "B")
    assert str(instruction) == "AND A B"


def test_springdroid_input_with_no_instructions_inputs_walk_command_as_ascii():
    spring_droid_input = SpringDroidInput(instructions=[])
    values = [spring_droid_input.read() for _ in range(5)]
    expected_values = [ord(c) for c in "WALK\n"]
    assert values == expected_values


def test_springdroid_input_raises_empty_buffer_error_if_trying_to_fetch_too_many_characters():
    spring_droid_input = SpringDroidInput(instructions=[])
    _ = [spring_droid_input.read() for _ in range(5)]
    with pytest.raises(SpringDroidInput.EmptyBufferError):
        spring_droid_input.read()


def test_springdroid_input_yields_instructions_separated_by_new_line_and_walk_command_as_ascii():
    spring_droid_input = SpringDroidInput(
        instructions=[
            SpringScriptInstruction(SpringScriptInstructionType.AND, "A", "B"),
            SpringScriptInstruction(SpringScriptInstructionType.OR, "C", "D"),
        ]
    )
    expected_stream = "AND A B\nOR C D\nWALK\n"
    values = [spring_droid_input.read() for _ in range(20)]
    expected_values = [ord(c) for c in expected_stream]
    assert values == expected_values
