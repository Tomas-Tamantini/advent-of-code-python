import pytest

from ..build_design import num_ways_to_make_design


@pytest.mark.parametrize(
    ("design", "num_ways"),
    [
        ("brwrr", 2),
        ("bggr", 1),
        ("gbbr", 4),
        ("rrbgbr", 6),
        ("bwurrg", 1),
        ("brgr", 2),
        ("ubwu", 0),
        ("bbrgwb", 0),
    ],
)
def test_design_is_possible_if_some_combination_of_patterns_yields_it(design, num_ways):
    available_patterns = ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]
    assert num_ways == num_ways_to_make_design(design, available_patterns)


def test_num_ways_to_build_design_is_calculated_efficiently():
    design = "a" * 30
    available_patterns = ["a", "aa"]
    assert 1346269 == num_ways_to_make_design(design, available_patterns)
