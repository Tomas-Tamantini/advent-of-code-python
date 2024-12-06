from models.common.io import InputFromString

from ..parser import parse_string_scrambler


def test_parse_string_scrambler_functions():
    file_content = """swap position 4 with position 0
                      swap letter d with letter b
                      reverse positions 0 through 4
                      rotate left 2 steps
                      rotate right 1 step
                      move position 1 to position 4
                      move position 3 to position 0
                      rotate based on position of letter b
                      rotate based on position of letter d"""
    scrambler = parse_string_scrambler(InputFromString(file_content))
    assert scrambler.scramble("abcde") == "decab"
