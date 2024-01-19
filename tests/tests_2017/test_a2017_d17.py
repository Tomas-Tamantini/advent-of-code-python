from models.aoc_2017 import CircularBuffer


def test_buffer_starts_with_single_zero_value():
    buffer = CircularBuffer()
    assert buffer.value_at_current_position == 0


def test_inserting_number_updates_current_position():
    buffer = CircularBuffer()
    buffer.insert_and_update_current_position(value=123, offset=3)
    assert buffer.value_at_current_position == 123


def test_numbers_are_inserted_in_front_of_current_position_plus_offset():
    buffer = CircularBuffer()
    offset = 3
    for i in range(1, 10):
        buffer.insert_and_update_current_position(i, offset)
    assert buffer.values == [9, 5, 7, 2, 4, 3, 8, 6, 1, 0]


def test_can_calculate_what_number_is_after_zero_after_sequential_inserts():
    assert CircularBuffer.value_after_zero(offset=3, insertions=1) == 1
    assert CircularBuffer.value_after_zero(offset=3, insertions=2) == 2
    assert CircularBuffer.value_after_zero(offset=3, insertions=3) == 2
    assert CircularBuffer.value_after_zero(offset=3, insertions=4) == 2
    assert CircularBuffer.value_after_zero(offset=3, insertions=5) == 5
    assert CircularBuffer.value_after_zero(offset=3, insertions=6) == 5
    assert CircularBuffer.value_after_zero(offset=3, insertions=7) == 5
    assert CircularBuffer.value_after_zero(offset=3, insertions=8) == 5
    assert CircularBuffer.value_after_zero(offset=3, insertions=9) == 9
