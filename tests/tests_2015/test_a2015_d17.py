from models.aoc_2015 import eggnog_partition


def test_eggnog_with_zero_volume_can_be_stored_in_one_way():
    assert list(eggnog_partition(0, [1, 2, 3])) == [[]]


def test_eggnog_with_volume_equal_to_smallest_container_can_be_stored_in_one_way():
    assert list(eggnog_partition(1, [1, 2, 3])) == [[1]]


def test_containers_with_the_same_capacity_are_considered_to_be_different():
    assert list(eggnog_partition(1, [1, 1])) == [[1], [1]]


def test_all_possible_eggnog_partitions_are_considered():
    assert len(list(eggnog_partition(25, [20, 15, 10, 5, 5]))) == 4
