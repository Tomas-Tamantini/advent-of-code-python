import pytest

from ..logic import HaltOutput3Bit, SerialOutput3Bit


def test_serial_output_3_bit_returns_output_values_separated_by_comma():
    serial_output = SerialOutput3Bit()
    serial_output.write(1)
    serial_output.write(2)
    serial_output.write(3)
    assert serial_output.get_output() == "1,2,3"


def test_halt_output_raises_stop_iteration_error_after_receiving_first_output():
    halt_output = HaltOutput3Bit()
    with pytest.raises(StopIteration):
        halt_output.write(123)
    assert halt_output.output_value == 123
