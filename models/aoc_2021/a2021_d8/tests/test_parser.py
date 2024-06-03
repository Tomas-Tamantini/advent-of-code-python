from models.common.io import InputFromString
from ..parser import parse_shuffled_seven_digit_displays
from ..seven_segment_display import ShuffledSevenDigitDisplay


def test_parse_shuffled_seven_digit_displays():
    file_content = """
                   cefbd dcg dcfgbae | cebdg egcfda
                   aefgc bcdgef bf bfaecd | gefac fgaec bdaf"""
    displays = list(parse_shuffled_seven_digit_displays(InputFromString(file_content)))
    assert displays == [
        ShuffledSevenDigitDisplay(
            unique_patterns=("cefbd", "dcg", "dcfgbae"),
            four_digit_output=("cebdg", "egcfda"),
        ),
        ShuffledSevenDigitDisplay(
            unique_patterns=("aefgc", "bcdgef", "bf", "bfaecd"),
            four_digit_output=("gefac", "fgaec", "bdaf"),
        ),
    ]
