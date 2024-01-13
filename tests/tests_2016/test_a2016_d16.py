import pytest
from models.aoc_2016 import DragonChecksum


@pytest.mark.parametrize(
    "input, expected",
    [
        ("1", "100"),
        ("0", "001"),
        ("11111", "11111000000"),
        ("111100001010", "1111000010100101011110000"),
    ],
)
def test_can_calculate_iterations_of_the_dragon_curve_algorithm(input, expected):
    assert DragonChecksum.dragon_curve(input) == expected


@pytest.mark.parametrize(
    "disk_space, input, expected",
    [
        (12, "110010110100", "100"),
        (20, "10000", "01100"),
    ],
)
def test_checksum_is_calculated_properly(disk_space, input, expected):
    checksum_calculator = DragonChecksum(disk_space)
    assert checksum_calculator.checksum(input) == expected
