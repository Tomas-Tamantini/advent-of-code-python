from typing import Iterable, Callable


class StringClassifier:
    def __init__(self, ruleset: Iterable[Callable[[str], bool]]) -> None:
        self._ruleset = ruleset

    def is_nice_string(self, string: str) -> bool:
        return all(rule(string) for rule in self._ruleset)


def string_contains_at_least_three_vowels(string: str) -> bool:
    vowels = [c for c in string if c in "aeiou"]
    return len(vowels) >= 3


def string_contains_at_least_one_letter_twice_in_a_row(string: str) -> bool:
    return any(string[i] == string[i + 1] for i in range(len(string) - 1))


def string_contains_disallowed_substrings(
    string: str, disallowed_substrings: set[str]
) -> bool:
    return any(substring in string for substring in disallowed_substrings)


def string_contains_pair_of_letters_twice(string: str) -> bool:
    return any(string[i : i + 2] in string[i + 2 :] for i in range(len(string) - 2))


def string_contains_letter_that_repeats_with_one_character_in_between(
    string: str,
) -> bool:
    return any(string[i] == string[i + 2] for i in range(len(string) - 2))


simple_ruleset = [
    string_contains_at_least_three_vowels,
    string_contains_at_least_one_letter_twice_in_a_row,
    lambda s: not string_contains_disallowed_substrings(s, {"ab", "cd", "pq", "xy"}),
]


complex_ruleset = [
    string_contains_pair_of_letters_twice,
    string_contains_letter_that_repeats_with_one_character_in_between,
]
