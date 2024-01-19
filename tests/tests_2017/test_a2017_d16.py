from models.aoc_2017 import Spin, Exchange, Partner


def test_spin_rolls_string_to_the_left():
    assert Spin(3).transform("abcde") == "cdeab"


def test_exchange_swaps_two_positions():
    assert Exchange(3, 4).transform("eabcd") == "eabdc"


def test_partner_swaps_two_characters():
    assert Partner("e", "b").transform("eabdc") == "baedc"
