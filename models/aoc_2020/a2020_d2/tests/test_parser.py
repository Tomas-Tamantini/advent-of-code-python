from models.common.io import InputFromString
from ..parser import parse_password_policies_and_passwords
from ..password_policy import RangePasswordPolicy, PositionalPasswordPolicy


def test_parse_pairs_of_range_password_policy_and_password():
    file_content = """
                   1-3 a: abcde
                   1-3 b: cdefg
                   2-9 c: ccccccccc
                   """
    pairs = list(
        parse_password_policies_and_passwords(
            InputFromString(file_content), use_range_policy=True
        )
    )
    assert pairs == [
        (
            RangePasswordPolicy(letter="a", min_occurrences=1, max_occurrences=3),
            "abcde",
        ),
        (
            RangePasswordPolicy(letter="b", min_occurrences=1, max_occurrences=3),
            "cdefg",
        ),
        (
            RangePasswordPolicy(letter="c", min_occurrences=2, max_occurrences=9),
            "ccccccccc",
        ),
    ]


def test_parse_pairs_of_positional_password_policy_and_password():
    file_content = """
                   1-3 a: abcde
                   1-3 b: cdefg
                   2-9 c: ccccccccc
                   """
    pairs = list(
        parse_password_policies_and_passwords(
            InputFromString(file_content), use_range_policy=False
        )
    )
    assert pairs == [
        (
            PositionalPasswordPolicy(letter="a", first_position=1, second_position=3),
            "abcde",
        ),
        (
            PositionalPasswordPolicy(letter="b", first_position=1, second_position=3),
            "cdefg",
        ),
        (
            PositionalPasswordPolicy(letter="c", first_position=2, second_position=9),
            "ccccccccc",
        ),
    ]
