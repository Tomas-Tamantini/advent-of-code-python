import pytest

from .solution import next_in_sequence, previous_in_sequence


@pytest.mark.parametrize(
    ("sequence", "expected"),
    [
        ((0, 0, 0), 0),
        ((0, 3, 6, 9, 12, 15), 18),
        ((1, 3, 6, 10, 15, 21), 28),
        ((10, 13, 16, 21, 30, 45), 68),
        ((1, -1, 2, -2), -25),
    ],
)
def test_next_in_sequence_extrapolates_using_newton_forward_difference(
    sequence, expected
):
    assert expected == next_in_sequence(sequence)


@pytest.mark.parametrize(
    ("sequence", "expected"),
    [
        ((13, 13, 13), 13),
        ((0, 3, 6, 9, 12, 15), -3),
        ((1, 3, 6, 10, 15, 21), 0),
        ((10, 13, 16, 21, 30, 45, 68), 5),
        ((1, -1, 2, -2), 20),
    ],
)
def test_previous_in_sequence_extrapolates_using_newton_backward_difference(
    sequence, expected
):
    assert expected == previous_in_sequence(sequence)
