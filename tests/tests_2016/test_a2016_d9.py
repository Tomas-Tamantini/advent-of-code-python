import pytest
from models.aoc_2016 import TextDecompressor


def test_text_without_markers_is_not_compressed():
    text = "ADVENT"
    decompressor = TextDecompressor(text)
    assert decompressor.length_decompressed() == len(text)


def test_text_with_marker_is_decompressed():
    text = "A(1x5)BC"
    decompressor = TextDecompressor(text)
    assert decompressor.length_decompressed() == 7


def test_invalid_markers_are_not_considered():
    text = "(16x7)(1x3)A"
    decompressor = TextDecompressor(text)
    assert decompressor.length_decompressed() == 42

    text = "X(8x2)(3x3)ABCY"
    decompressor = TextDecompressor(text)
    assert decompressor.length_decompressed() == 18


@pytest.mark.parametrize(
    "text, expected_length",
    [
        ("ADVENT", 6),
        ("A(1x5)BC", 7),
        ("(3x3)XYZ", 9),
        ("A(2x2)BCD(2x2)EFG", 11),
        ("(6x1)(1x3)A", 6),
        ("X(8x2)(3x3)ABCY", 18),
        ("(20x12)(20x12)(13x14)(7x10)(1x12)A", 252),
        ("(20x12)(20x12)(13x14)(7x10)A(1x12)A", 253),
    ],
)
def test_texts_are_decompressed_properly(text, expected_length):
    decompressor = TextDecompressor(text)
    assert decompressor.length_decompressed() == expected_length
