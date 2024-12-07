import pytest

from .logic import (
    BeginDroidCommand,
    SpringDroidInput,
    SpringDroidOutput,
    SpringScriptInstruction,
    SpringScriptInstructionType,
    run_spring_droid_program,
)


def test_springscript_instruction_can_be_converted_to_string():
    instruction = SpringScriptInstruction(SpringScriptInstructionType.AND, "A", "B")
    assert str(instruction) == "AND A B"


@pytest.mark.parametrize(
    ("command", "command_str"),
    [(BeginDroidCommand.WALK, "WALK"), (BeginDroidCommand.RUN, "RUN")],
)
def test_springdroid_input_with_no_instructions_inputs_walk_or_run_command_as_ascii(
    command, command_str
):
    spring_droid_input = SpringDroidInput(instructions=[], begin_droid_command=command)
    values = [spring_droid_input.read() for _ in range(len(command_str) + 1)]
    expected_values = [ord(c) for c in f"{command_str}\n"]
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
    assert not spring_droid_output.render()


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


def test_running_springdroid_program_reads_springscript_inputs_and_writes_to_output():
    intcode_instructions = [3, 567, 4, 567, 104, 123456, 99]
    springscript_instructions = [
        SpringScriptInstruction(SpringScriptInstructionType.NOT, "A", "B"),
    ]
    droid_input = SpringDroidInput(springscript_instructions)
    droid_output = SpringDroidOutput()
    run_spring_droid_program(intcode_instructions, droid_input, droid_output)
    assert droid_output.render() == "N"  # First letter of NOT A B
    assert droid_output.large_output() == 123456
