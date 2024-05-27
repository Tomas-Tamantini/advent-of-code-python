import pytest
from .snail_fish import SnailfishNode, SnailfishLeaf, SnailFishTree


def test_snailfish_leaf_magnitude_is_its_value():
    leaf = SnailfishLeaf(value=123)
    assert leaf.magnitude() == 123


def test_snailfish_node_magnitude_is_three_times_magnitude_of_left_child_plus_two_times_magnitude_of_right_child():
    node = SnailfishNode(
        left_child=SnailfishLeaf(value=4), right_child=SnailfishLeaf(value=5)
    )
    assert node.magnitude() == 22


def test_snailfish_magnitude_is_calculated_recursively():
    tree = SnailFishTree.from_list([[[[5, 0], [7, 4]], [5, 5]], [6, 6]])
    assert tree.magnitude() == 1137


def test_snailfish_with_number_ten_or_greater_splits_number_into_pair():
    tree = SnailFishTree.from_list([5, 11])
    tree.reduce()
    assert tree.to_list() == [5, [5, 6]]


def test_snailfish_splits_numbers_recursively():
    tree = SnailFishTree.from_list([13, 22])
    tree.reduce()
    assert tree.to_list() == [[6, 7], [[5, 6], [5, 6]]]


@pytest.mark.parametrize(
    "before_reduce, after_reduce",
    [
        ([[[[[9, 8], 1], 2], 3], 4], [[[[0, 9], 2], 3], 4]),
        ([7, [6, [5, [4, [3, 2]]]]], [7, [6, [5, [7, 0]]]]),
        ([[6, [5, [4, [3, 2]]]], 1], [[6, [5, [7, 0]]], 3]),
        (
            [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
        ),
        (
            [[3, [2, [8, 0]]], [9, [5, [4, [3, 2]]]]],
            [[3, [2, [8, 0]]], [9, [5, [7, 0]]]],
        ),
    ],
)
def test_snailfish_pair_nested_more_than_four_levels_down_gets_exploded(
    before_reduce, after_reduce
):
    tree = SnailFishTree.from_list(before_reduce)
    tree.reduce()
    assert tree.to_list() == after_reduce


def test_snailfish_pair_does_explosions_and_splits_until_no_further_reduction_is_possilbe():
    tree = SnailFishTree.from_list([[[[[4, 3], 4], 4], [7, [[8, 4], 9]]], [1, 1]])
    tree.reduce()
    assert tree.to_list() == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]


def test_adding_snailfish_pairs_puts_them_together_in_larger_pair():
    tree_a = SnailFishTree.from_list([5, 6])
    tree_b = SnailFishTree.from_list([7, 8])
    tree_c = tree_a + tree_b
    assert tree_c.to_list() == [[5, 6], [7, 8]]


def test_adding_snailfish_numbers_automatically_reduces_them():
    tree_a = SnailFishTree.from_list([[[[4, 3], 4], 4], [7, [[8, 4], 9]]])
    tree_b = SnailFishTree.from_list([1, 1])
    tree_c = tree_a + tree_b
    assert tree_c.to_list() == [[[[0, 7], 4], [[7, 8], [6, 0]]], [8, 1]]
