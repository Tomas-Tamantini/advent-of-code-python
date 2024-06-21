import pytest
from .solution import snafu_to_decimal, decimal_to_snafu


@pytest.mark.parametrize(
    "decimal, snafu",
    [
        (0, "0"),
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (7, "12"),
        (8, "2="),
        (9, "2-"),
        (10, "20"),
        (15, "1=0"),
        (20, "1-0"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0"),
    ],
)
def test_snafu_numbers_can_be_converted_to_decimal_and_vice_versa(decimal, snafu):
    assert snafu_to_decimal(snafu) == decimal
    assert decimal_to_snafu(decimal) == snafu
