from models.aoc_2017 import Spin, Exchange, Partner, transform_string_multiple_rounds


def test_spin_rolls_string_to_the_left():
    assert Spin(3).transform("abcde") == "cdeab"


def test_exchange_swaps_two_positions():
    assert Exchange(3, 4).transform("eabcd") == "eabdc"


def test_partner_swaps_two_characters():
    assert Partner("e", "b").transform("eabdc") == "baedc"


def test_transforming_string_zero_rounds_returns_same_string():
    assert transform_string_multiple_rounds("abcde", [], num_rounds=0) == "abcde"


def test_all_transformations_in_order_count_as_one_round():
    assert (
        transform_string_multiple_rounds(
            "abcde",
            [Spin(1), Exchange(3, 4), Partner("e", "b")],
            num_rounds=1,
        )
        == "baedc"
    )


def test_multiple_rounds_of_transformation_are_performed_efficiently():
    assert (
        transform_string_multiple_rounds(
            "abcde",
            [Spin(1), Exchange(3, 4), Partner("e", "b")],
            num_rounds=1_000_000_001,
        )
        == "baedc"
    )
