from .circular_encryption import mix_list


def test_mixing_list_shifts_numbers_by_appropriate_offsets():
    lst = [1, 2, -3, 3, -2, 0, 4]
    expected = [1, 2, -3, 4, 0, 3, -2]
    assert expected == mix_list(lst)


def test_list_can_be_mixed_multiple_rounds_efficiently():
    lst = [811589153, 1623178306, -2434767459, 2434767459, -1623178306, 0, 3246356612]
    res = [811589153, 0, -2434767459, 1623178306, 3246356612, -1623178306, 2434767459]
    assert res == mix_list(lst, num_rounds=10)
