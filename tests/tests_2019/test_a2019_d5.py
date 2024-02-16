from models.aoc_2019 import (
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
    sequence = [3, 0, 4, 0, 99]
    air_conditioner_id = 123
    serial_input = AirConditionerSerialInput(air_conditioner_id)
    serial_output = AirConditionerSerialOutput()
    run_air_conditioner_program(sequence, serial_input, serial_output)
    assert serial_output.peek() == air_conditioner_id
