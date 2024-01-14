from models.aoc_2016 import DisjoinIntervals


def test_disjoint_intervals_starts_with_single_interval():
    disjoint_intervals = DisjoinIntervals(1, 10)
    assert list(disjoint_intervals.intervals()) == [(1, 10)]


def test_removing_interval_outside_original_one_does_nothing():
    disjoint_intervals = DisjoinIntervals(1, 10)
    disjoint_intervals.remove(11, 20)
    assert list(disjoint_intervals.intervals()) == [(1, 10)]


def test_removing_interval_can_make_original_one_smaller():
    disjoint_intervals = DisjoinIntervals(1, 10)
    disjoint_intervals.remove(1, 5)
    assert list(disjoint_intervals.intervals()) == [(6, 10)]


def test_removing_interval_can_cut_original_one_in_two():
    disjoint_intervals = DisjoinIntervals(1, 10)
    disjoint_intervals.remove(3, 8)
    assert list(disjoint_intervals.intervals()) == [(1, 2), (9, 10)]


def test_multiple_intervals_can_be_removed():
    disjoint_intervals = DisjoinIntervals(1, 10)
    disjoint_intervals.remove(10, 1000)
    disjoint_intervals.remove(8, 8)
    disjoint_intervals.remove(3, 5)
    disjoint_intervals.remove(3, 4)
    assert list(disjoint_intervals.intervals()) == [
        (1, 2),
        (6, 7),
        (9, 9),
    ]


def test_can_query_number_of_elements_in_intervals():
    disjoint_intervals = DisjoinIntervals(1, 10)
    disjoint_intervals.remove(10, 1000)
    disjoint_intervals.remove(8, 8)
    disjoint_intervals.remove(3, 5)
    disjoint_intervals.remove(3, 4)
    assert disjoint_intervals.num_elements() == 5
