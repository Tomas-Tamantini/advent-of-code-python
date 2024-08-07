from ..logic import CubeAmount


def test_cube_amount_checks_if_all_colors_are_leq_colors_from_other_amount():
    amount_a = CubeAmount({"red": 1, "green": 2})
    amount_b = CubeAmount({"red": 2, "green": 2, "blue": 10})
    assert amount_a.all_colors_leq(amount_b)
    assert not amount_b.all_colors_leq(amount_a)


def test_merging_cube_amounts_keeps_maximum_amount_for_each_color():
    amount_a = CubeAmount({"red": 1, "green": 5})
    amount_b = CubeAmount({"red": 2, "green": 2, "blue": 10})
    merged = CubeAmount.merge(amount_a, amount_b)
    assert merged.amount_by_color == {"red": 2, "green": 5, "blue": 10}
