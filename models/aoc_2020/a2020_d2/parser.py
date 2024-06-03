from typing import Iterator
from models.common.io import InputReader
from .password_policy import (
    PasswordPolicy,
    RangePasswordPolicy,
    PositionalPasswordPolicy,
)


def _parse_password_policy_and_password(
    line: str, use_range_policy: bool
) -> tuple[PasswordPolicy, str]:
    parts = line.split(":")
    policy_parts = parts[0].split(" ")
    num_a, num_b = map(int, policy_parts[0].split("-"))
    letter = policy_parts[1]
    password = parts[1].strip()
    if use_range_policy:
        return RangePasswordPolicy(letter, num_a, num_b), password
    else:
        return PositionalPasswordPolicy(letter, num_a, num_b), password


def parse_password_policies_and_passwords(
    input_reader: InputReader, use_range_policy: bool
) -> Iterator[tuple[PasswordPolicy, str]]:
    for line in input_reader.read_stripped_lines():
        yield _parse_password_policy_and_password(line, use_range_policy)
