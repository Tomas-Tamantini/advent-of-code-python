from typing import Iterator


def contains_exactly_n_of_any_letter(string: str, n: int) -> bool:
    return any(string.count(letter) == n for letter in string)


def differing_indices(string_a: str, string_b: str) -> Iterator[int]:
    for index, (a, b) in enumerate(zip(string_a, string_b)):
        if a != b:
            yield index
