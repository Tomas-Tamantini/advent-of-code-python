import pytest

from ..build_design import design_is_possible

_AVAILABLE_PATTERNS = ["r", "wr", "b", "g", "bwu", "rb", "gb", "br"]


@pytest.mark.parametrize(
    "design",
    ["brwrr", "bggr", "gbbr", "rrbgbr", "bwurrg", "brgr"],
)
def test_design_is_possible_if_some_combination_of_patterns_yields_it(design):
    assert design_is_possible(design, _AVAILABLE_PATTERNS)


@pytest.mark.parametrize(
    "design",
    ["ubwu", "bbrgwb"],
)
def test_design_is_impossible_if_no_combination_of_patterns_yields_it(design):
    assert not design_is_possible(design, _AVAILABLE_PATTERNS)
