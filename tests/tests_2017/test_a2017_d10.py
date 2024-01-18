import pytest
from models.aoc_2017 import KnotHash


def test_knot_hash_initializes_with_a_sorted_list():
    knot_hash = KnotHash(list_length=5)
    assert knot_hash.list == [0, 1, 2, 3, 4]


@pytest.mark.parametrize("length", [0, 1])
def test_hashing_with_length_zero_or_one_does_nothing(length):
    knot_hash = KnotHash(list_length=5)
    knot_hash.iterate_hash(length)
    assert knot_hash.list == [0, 1, 2, 3, 4]


def test_first_iteration_operates_from_current_position_as_zero():
    knot_hash = KnotHash(5)
    knot_hash.iterate_hash(length=3)
    assert knot_hash.list == [2, 1, 0, 3, 4]


def test_current_position_increments_by_length_on_second_iteration():
    knot_hash = KnotHash(5)
    knot_hash.iterate_hash(length=3)
    knot_hash.iterate_hash(length=4)
    assert knot_hash.list == [4, 3, 0, 1, 2]


def test_current_position_increments_by_length_plus_skip_size_of_one_on_third_iteration():
    knot_hash = KnotHash(5)
    knot_hash.iterate_hash(length=3)
    knot_hash.iterate_hash(length=4)
    knot_hash.iterate_hash(length=2)
    assert knot_hash.list == [4, 3, 0, 2, 1]


def test_skip_size_increases_by_one_at_each_iteration():
    knot_hash = KnotHash(5)
    knot_hash.iterate_hash(length=3)
    knot_hash.iterate_hash(length=4)
    knot_hash.iterate_hash(length=1)
    knot_hash.iterate_hash(length=5)
    assert knot_hash.list == [3, 4, 2, 1, 0]


def test_dense_hash_is_each_group_of_16_numbers_xorred():
    knot_hash = KnotHash(256)
    for length in [17, 31, 73, 47, 23] * 64:
        knot_hash.iterate_hash(length)
    dense_hash = knot_hash.dense_hash()
    assert list(dense_hash)[0:3] == [0xA2, 0x58, 0x2A]
