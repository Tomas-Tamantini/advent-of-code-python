from .digit_finder import Digit, find_digits


def test_digit_finder_finds_digits_and_their_position():
    sequence = "a1bc87dtwo"
    digits = list(find_digits(sequence))
    assert digits == [
        Digit(position=1, value=1),
        Digit(position=4, value=8),
        Digit(position=5, value=7),
    ]


def test_digit_finder_finds_spelled_out_digits():
    sequence = "atwob9cseventy"
    digits = list(find_digits(sequence, include_spelled_out=True))
    assert digits == [
        Digit(position=1, value=2),
        Digit(position=5, value=9),
        Digit(position=7, value=7),
    ]
