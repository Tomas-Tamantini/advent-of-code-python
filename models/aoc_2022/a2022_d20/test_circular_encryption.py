from .circular_encryption import mix_list


def test_mixing_list_shifts_numbers_by_appropriate_offsets():
    lst = [1, 2, -3, 3, -2, 0, 4]
    expected = [1, 2, -3, 4, 0, 3, -2]
    assert mix_list(lst) == expected
