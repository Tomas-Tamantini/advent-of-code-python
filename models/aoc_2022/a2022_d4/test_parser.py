from models.common.io import InputFromString
from models.common.number_theory import Interval

from .parser import parse_interval_pairs


def test_parse_interval_pairs():
    input_reader = InputFromString(
        """
        2-4,6-8
        2-3,4-5
        """
    )
    pairs = list(parse_interval_pairs(input_reader))
    assert pairs == [
        (Interval(2, 4), Interval(6, 8)),
        (Interval(2, 3), Interval(4, 5)),
    ]
