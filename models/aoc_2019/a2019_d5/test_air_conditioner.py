from .air_conditioner import (
    AirConditionerSerialInput,
    AirConditionerSerialOutput,
    run_air_conditioner_program,
)


def test_air_conditioner_serial_input_reads_air_conditioner_id():
    air_conditioner_id = 123
    serial_input = AirConditionerSerialInput(air_conditioner_id)
    assert serial_input.read() == air_conditioner_id


def test_air_conditioner_serial_output_starts_empty():
    serial_output = AirConditionerSerialOutput()
    assert serial_output.peek() is None


def test_air_conditioner_serial_output_stores_written_values():
    serial_output = AirConditionerSerialOutput()
    serial_output.write(123)
    assert serial_output.peek() == 123
    serial_output.write(456)
    assert serial_output.peek() == 456


def test_air_conditioner_program_writes_to_serial_output():
    instructions = [3, 0, 4, 0, 99]
    air_conditioner_id = 123
    output = run_air_conditioner_program(instructions, air_conditioner_id)
    assert output == air_conditioner_id
