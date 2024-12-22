from .pseudo_random import next_pseudo_random


def test_next_pseudo_random():
    current = 123
    expected = 15887950
    assert next_pseudo_random(current) == expected
