from models.aoc_2015 import next_look_and_say


def test_look_and_say_sequence_has_fixed_point():
    assert next_look_and_say("22") == "22"


def test_look_and_say_sequence_properly_calculates_next_term():
    assert next_look_and_say("111221") == "312211"
