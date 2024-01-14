import pytest
from models.aoc_2016 import (
    StringScrambler,
    MultiStepScrambler,
    LetterSwapScrambler,
    PositionSwapScrambler,
    RotationScrambler,
    LetterBasedRotationScrambler,
    ReversionScrambler,
    LetterMoveScrambler,
)


@pytest.mark.parametrize(
    "scrambler, original, scrambled",
    [
        (PositionSwapScrambler(0, 4), "abcde", "ebcda"),
        (PositionSwapScrambler(4, 0), "abcde", "ebcda"),
        (PositionSwapScrambler(1, 3), "abcde", "adcbe"),
        (LetterSwapScrambler("d", "b"), "ebcda", "edcba"),
        (RotationScrambler(0), "abcde", "abcde"),
        (RotationScrambler(3), "abcde", "cdeab"),
        (RotationScrambler(-2), "abcde", "cdeab"),
        (ReversionScrambler(0, 4), "edcba", "abcde"),
        (ReversionScrambler(1, 3), "ebcda", "edcba"),
        (LetterMoveScrambler(1, 4), "bcdea", "bdeac"),
        (LetterMoveScrambler(3, 1), "bdeac", "badec"),
        (LetterBasedRotationScrambler("f"), "abcdefgh", "bcdefgha"),
    ],
)
def test_scrambles_can_be_done_and_undone(scrambler, original, scrambled):
    assert scrambler.scramble(original) == scrambled
    assert scrambler.unscramble(scrambled) == original


def test_rotates_one_plus_idx_of_letter_before_idx_four():
    assert LetterBasedRotationScrambler("a").scramble("abcde") == "eabcd"
    assert LetterBasedRotationScrambler("b").scramble("abcde") == "deabc"
    assert LetterBasedRotationScrambler("c").scramble("abcde") == "cdeab"
    assert LetterBasedRotationScrambler("d").scramble("abcde") == "bcdea"


def test_rotates_two_plus_idx_of_letter_before_after_idx_three():
    assert LetterBasedRotationScrambler("e").scramble("abcdef") == "abcdef"
    assert LetterBasedRotationScrambler("f").scramble("abcdef") == "fabcde"


def test_multi_step_scrambler_applies_all_steps_in_order():
    scrambler = MultiStepScrambler(
        [
            PositionSwapScrambler(4, 0),
            LetterSwapScrambler("d", "b"),
            RotationScrambler(3),
            ReversionScrambler(0, 4),
        ]
    )
    assert scrambler.scramble("abcde") == "deabc"
    assert scrambler.unscramble("deabc") == "abcde"
