import pytest
from .packet_comparison import left_packet_leq_right


@pytest.mark.parametrize(
    "left_packet, right_packet, expected",
    [(1, 2, True), (123, 123, True), (7, 5, False)],
)
def test_if_both_packets_are_integers_they_are_compared_directly(
    left_packet, right_packet, expected
):
    assert left_packet_leq_right(left_packet, right_packet) == expected


@pytest.mark.parametrize(
    "left_packet, right_packet, expected",
    [
        ([1, 1, 3, 9], [1, 1, 5, 1], True),
        ([2, 1], [2, 1], True),
        ([5, 1], [2, 9], False),
        ([1, 1], [1, 1, 1], True),
        ([1, 1, 1, 1], [1, 1, 1], False),
    ],
)
def test_if_both_packets_are_lists_they_are_compared_lexicographically(
    left_packet, right_packet, expected
):
    assert left_packet_leq_right(left_packet, right_packet) == expected


@pytest.mark.parametrize(
    "left_packet, right_packet, expected",
    [
        (1, [1, 1, 5, 1], True),
        (2, [1, 1, 5, 1], False),
        ([7, 8], 9, True),
        ([8, 9], 6, False),
    ],
)
def test_if_exactly_one_packet_is_int_it_is_compared_as_list(
    left_packet, right_packet, expected
):
    assert left_packet_leq_right(left_packet, right_packet) == expected


@pytest.mark.parametrize(
    "left_packet, right_packet, expected",
    [
        ([[1], [2, 3, 4]], [[1], 4], True),
        ([9], [[8, 7, 6]], False),
        ([[4, 4], 4, 4], [[4, 4], 4, 4, 4], True),
        ([], [3], True),
        ([[[]]], [[]], False),
        (
            [1, [2, [3, [4, [5, 6, 7]]]], 8, 9],
            [1, [2, [3, [4, [5, 6, 0]]]], 8, 9],
            False,
        ),
    ],
)
def test_packet_comparison_is_done_recursively(left_packet, right_packet, expected):
    assert left_packet_leq_right(left_packet, right_packet) == expected
