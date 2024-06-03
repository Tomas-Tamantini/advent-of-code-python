from typing import Protocol
from dataclasses import dataclass


class BelongsToSetRule:
    def __init__(self, members: set[str]):
        self._members = members

    def is_valid(self, value: str) -> bool:
        return value in self._members


class ValidationRule(Protocol):
    def is_valid(self, value: str) -> bool: ...


@dataclass(frozen=True)
class RangeRule:
    inclusive_min: int
    inclusive_max: int

    def is_valid(self, value: str) -> bool:
        if not value.isdigit():
            return False
        else:
            return self.inclusive_min <= int(value) <= self.inclusive_max


@dataclass(frozen=True)
class HeightRule:
    min_cm: int
    max_cm: int
    min_in: int
    max_in: int

    def is_valid(self, value: str) -> bool:
        if len(value) < 3:
            return False
        height = value[:-2]
        if not height.isdigit():
            return False
        height = int(height)
        unit = value[-2:]
        if unit == "cm":
            return self.min_cm <= height <= self.max_cm
        elif unit == "in":
            return self.min_in <= height <= self.max_in
        else:
            return False


class HairColorRule:
    def is_valid(self, value: str) -> bool:
        return (
            len(value) == 7
            and value.startswith("#")
            and all(c in "0123456789abcdef" for c in value[1:])
        )


class PassportIdRule:
    def is_valid(self, value: str) -> bool:
        return len(value) == 9 and value.isdigit()


def passport_is_valid(
    passport: dict[str, str], rules: dict[str, ValidationRule]
) -> bool:
    for key, rule in rules.items():
        if key not in passport or not rule.is_valid(passport[key]):
            return False
    return True


PASSPORT_RULES = {
    "byr": RangeRule(1920, 2002),
    "iyr": RangeRule(2010, 2020),
    "eyr": RangeRule(2020, 2030),
    "hgt": HeightRule(min_cm=150, max_cm=193, min_in=59, max_in=76),
    "hcl": HairColorRule(),
    "ecl": BelongsToSetRule({"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}),
    "pid": PassportIdRule(),
}
