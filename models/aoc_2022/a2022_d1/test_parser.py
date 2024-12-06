from models.common.io import InputFromString

from .parser import parse_calories


def test_calories_are_grouped_by_line_break():
    input_reader = InputFromString(
        """
        12
        123

        5
        -6
        3

        1
        """
    )
    calories = list(parse_calories(input_reader))
    assert calories == [(12, 123), (5, -6, 3), (1,)]
