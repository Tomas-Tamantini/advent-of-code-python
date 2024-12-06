import pytest

from ..logic import HashCalculator


@pytest.mark.parametrize(
    ("text", "expected"), [("HASH", 52), ("rn=1", 30), ("pc=6", 214)]
)
def test_hash_of_a_string_is_calculated_properly(text, expected):
    text = "HASH"
    expected = 52
    calculator = HashCalculator()
    assert expected == calculator.get_hash(text)
