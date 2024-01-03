from models.aoc_2015 import next_look_and_say


def test_look_and_say_sequence_has_fixed_point():
    assert next_look_and_say([2, 2]) == [2, 2]


def test_look_and_say_sequence_properly_calculates_next_term():
    assert next_look_and_say([1, 1, 1, 2, 2, 1]) == [3, 1, 2, 2, 1, 1]
