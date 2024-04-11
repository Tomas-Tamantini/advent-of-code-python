import pytest
from models.aoc_2019.a2019_d21 import (
    SpringScriptInstruction,
    SpringScriptInstructionType,
    SpringDroidInput,
    SpringDroidOutput,
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


def test_springdroid_output_starts_empty():
    spring_droid_output = SpringDroidOutput()
    assert spring_droid_output.render() == ""


def test_springdroid_output_stores_ascii_values():
    spring_droid_output = SpringDroidOutput()
    spring_droid_output.write(65)
    spring_droid_output.write(66)
    spring_droid_output.write(10)
    spring_droid_output.write(67)
    assert spring_droid_output.render() == "AB\nC"


def test_springdroid_output_stores_value_larger_than_ascii_range_separately():
    spring_droid_output = SpringDroidOutput()
    spring_droid_output.write(65)
    spring_droid_output.write(123456)
    spring_droid_output.write(66)
    assert spring_droid_output.render() == "AB"
    assert spring_droid_output.large_output() == 123456


def test_springdroid_output_large_integer_must_be_stored_before_being_fetched():
    with pytest.raises(ValueError):
        _ = SpringDroidOutput().large_output()
