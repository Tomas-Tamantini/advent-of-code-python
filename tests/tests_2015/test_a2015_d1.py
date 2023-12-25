from models.aoc_2015 import first_basement


def test_returns_first_time_santa_reaches_basement():
    assert first_basement(")") == 1
    assert first_basement("()())") == 5
