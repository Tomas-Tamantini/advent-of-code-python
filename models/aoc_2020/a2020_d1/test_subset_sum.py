from .subset_sum import subsets_that_sum_to


def test_subsets_which_add_to_target_is_just_number_itself_if_subset_size_is_1():
    assert list(
        subsets_that_sum_to(target_sum=123, subset_size=1, entries=[1, 123, 2])
    ) == [(123,)]


def test_iterates_through_all_pairs_of_numbers_which_add_up_to_target():
    assert list(
        subsets_that_sum_to(target_sum=7, subset_size=2, entries=[1, 2, 3, 4, 5])
    ) == [(2, 5), (3, 4)]


def test_iterates_through_all_subsets_of_given_size_which_add_up_to_target():
    assert list(
        subsets_that_sum_to(target_sum=8, subset_size=3, entries=[1, 2, 3, 4, 5])
    ) == [
        (1, 2, 5),
        (1, 3, 4),
    ]
