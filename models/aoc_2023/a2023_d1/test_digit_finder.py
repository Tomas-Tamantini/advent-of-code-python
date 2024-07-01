from .digit_finder import find_digits, Digit


def test_digit_finder_finds_digits_and_their_position():
    sequence = "a1bc87d"
    digits = list(find_digits(sequence))
    assert digits == [
        Digit(position=1, value=1),
        Digit(position=4, value=8),
        Digit(position=5, value=7),
    ]
