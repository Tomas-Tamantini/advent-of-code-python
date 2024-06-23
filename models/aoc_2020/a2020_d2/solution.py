from models.common.io import IOHandler
from .parser import parse_password_policies_and_passwords


def aoc_2020_d2(io_handler: IOHandler, **_) -> None:
    print("--- AOC 2020 - Day 2: Password Philosophy ---")
    num_valid_range_passwords = sum(
        1
        for policy, password in parse_password_policies_and_passwords(
            io_handler.input_reader, use_range_policy=True
        )
        if policy.is_valid(password)
    )
    print(f"Part 1: {num_valid_range_passwords} valid passwords using range rule")

    num_valid_positional_passwords = sum(
        1
        for policy, password in parse_password_policies_and_passwords(
            io_handler.input_reader, use_range_policy=False
        )
        if policy.is_valid(password)
    )
    print(
        f"Part 2: {num_valid_positional_passwords} valid passwords using positional rule"
    )
