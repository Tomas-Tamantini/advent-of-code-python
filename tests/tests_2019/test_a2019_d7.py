import pytest
from models.aoc_2019.a2019_d7 import (
    AmplifierSerialInput,
    AmplifierSerialOutput,
    Amplifiers,
)


def test_amplifier_serial_input_works_as_queue():
    serial_input = AmplifierSerialInput()
    serial_input.put(1)
    serial_input.put(2)
    assert serial_input.read() == 1
    assert serial_input.read() == 2


def test_amplifier_serial_output_raises_stop_iteration_error_on_first_write():
    serial_output = AmplifierSerialOutput()
    with pytest.raises(StopIteration):
        serial_output.write(1)
    assert serial_output.read() == 1


@pytest.mark.parametrize(
    "program, phase_settings, expected_output",
    [
        (
            [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0],
            [4, 3, 2, 1, 0],
            43210,
        ),
        (
            [
                3,
                23,
                3,
                24,
                1002,
                24,
                10,
                24,
                1002,
                23,
                -1,
                23,
                101,
                5,
                23,
                23,
                1,
                24,
                23,
                23,
                4,
                23,
                99,
                0,
                0,
            ],
            [0, 1, 2, 3, 4],
            54321,
        ),
        (
            [
                3,
                31,
                3,
                32,
                1002,
                32,
                10,
                32,
                1001,
                31,
                -2,
                31,
                1007,
                31,
                0,
                33,
                1002,
                33,
                7,
                33,
                1,
                33,
                31,
                31,
                1,
                32,
                31,
                31,
                4,
                31,
                99,
                0,
                0,
                0,
            ],
            [1, 0, 4, 3, 2],
            65210,
        ),
    ],
)
def test_amplifiers_produce_final_output_given_phase_settings_and_input_signal(
    program, phase_settings, expected_output
):
    amplifiers = Amplifiers(program)
    input_signal = 0
    final_output = amplifiers.run(phase_settings, input_signal)
    assert final_output == expected_output
