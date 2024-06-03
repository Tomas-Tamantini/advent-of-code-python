from ..seven_segment_display import ShuffledSevenDigitDisplay


def test_decoding_shuffled_seven_digit_display_yields_four_digit_output():
    display = ShuffledSevenDigitDisplay(
        unique_patterns=(
            "be",
            "cfbegad",
            "cbdgef",
            "fgaecd",
            "cgeb",
            "fdcge",
            "agebfd",
            "fecdb",
            "fabcd",
            "edb",
        ),
        four_digit_output=("fdgacbe", "cefdb", "cefbgd", "gcbe"),
    )
    assert display.decode() == "8394"
