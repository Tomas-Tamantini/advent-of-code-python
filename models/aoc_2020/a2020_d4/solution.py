from models.common.io import IOHandler
from .parser import parse_passports
from .passport import PASSPORT_RULES, passport_is_valid


def aoc_2020_d4(io_handler: IOHandler) -> None:
    print("--- AOC 2020 - Day 4: Passport Processing ---")
    passports = list(parse_passports(io_handler.input_reader))
    required_fields = set(PASSPORT_RULES.keys())
    passports_with_all_fields = [
        passport for passport in passports if required_fields.issubset(passport.keys())
    ]
    print(f"Part 1: {len(passports_with_all_fields)} passports with all fields")

    num_valid_passports = sum(
        passport_is_valid(passport, PASSPORT_RULES) for passport in passports
    )
    print(f"Part 2: {num_valid_passports} valid passports")
