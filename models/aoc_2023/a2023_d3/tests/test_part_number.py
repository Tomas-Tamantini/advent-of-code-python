from ..logic import PartNumber


def test_part_number_spans_as_many_columns_as_characters():
    part_number = PartNumber(serial="123", row=0, start_column=0)
    assert part_number.end_column == 2


def test_part_number_value_is_serial_converted_to_int():
    part_number = PartNumber(serial="0123", row=0, start_column=0)
    assert part_number.number == 123
