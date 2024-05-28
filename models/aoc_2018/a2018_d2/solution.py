from typing import Iterator
from itertools import combinations
from models.common.io import InputReader


def contains_exactly_n_of_any_letter(string: str, n: int) -> bool:
    return any(string.count(letter) == n for letter in string)


def differing_indices(string_a: str, string_b: str) -> Iterator[int]:
    for index, (a, b) in enumerate(zip(string_a, string_b)):
        if a != b:
            yield index


def aoc_2018_d2(input_reader: InputReader, **_) -> None:
    print("--- AOC 2018 - Day 2: Inventory Management System ---")
    lines = list(input_reader.readlines())
    ids = [line.strip() for line in lines]
    exactly_two = sum(contains_exactly_n_of_any_letter(id, 2) for id in ids)
    exactly_three = sum(contains_exactly_n_of_any_letter(id, 3) for id in ids)
    print(f"Part 1: Checksum of ids is {exactly_two * exactly_three}")
    letters_in_common = ""
    for i, j in combinations(range(len(ids)), 2):
        differing = list(differing_indices(ids[i], ids[j]))
        if len(differing) == 1:
            letters_in_common = ids[i][: differing[0]] + ids[i][differing[0] + 1 :]
            break

    print(f"Part 2: Letters in common between ids are {letters_in_common}")
