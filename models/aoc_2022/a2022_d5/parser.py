from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator

from models.common.io import InputReader

from .logic import Crate, MoveCratesMultipleAtATime, MoveCratesOneAtATime


@dataclass
class _ParsedCrates:
    crates: dict[int, Crate]
    moves: list[MoveCratesOneAtATime]


def _non_empty_lines(input_reader: InputReader):
    for line in input_reader.readlines():
        if line.strip():
            yield line


def _parse_move(line: str, move_one_at_a_time: bool) -> MoveCratesOneAtATime:
    stripped_line = line.strip()
    move_parts = stripped_line.split()
    move_cls = MoveCratesOneAtATime if move_one_at_a_time else MoveCratesMultipleAtATime
    return move_cls(*(int(move_parts[i]) for i in (3, 5, 1)))


def _upper_case_letters(line: str) -> Iterator[tuple[int, chr]]:
    for i, char in enumerate(line):
        if char.isupper():
            yield i, char


def _digits(line: str) -> Iterator[tuple[int, int]]:
    for i, char in enumerate(line):
        if char.isdigit():
            yield i, int(char)


def _create_crates(
    positions_to_crate_ids: dict[int, int], positions_to_items: dict[int, list[chr]]
) -> dict[int, Crate]:
    crates = dict()
    for position, crate_id in positions_to_crate_ids.items():
        crate = Crate()
        for item in reversed(positions_to_items[position]):
            crate.push(item)
        crates[crate_id] = crate
    return crates


def parse_crates(input_reader: InputReader, move_one_at_a_time: bool) -> _ParsedCrates:
    moves = []
    positions_to_crate_ids = dict()
    positions_to_items = defaultdict(list)
    for line in _non_empty_lines(input_reader):
        if "move" in line:
            moves.append(_parse_move(line, move_one_at_a_time))
        elif "[" in line:
            for i, char in _upper_case_letters(line):
                positions_to_items[i].append(char)
        else:
            for i, digit in _digits(line):
                positions_to_crate_ids[i] = digit

    crates = _create_crates(positions_to_crate_ids, positions_to_items)
    return _ParsedCrates(crates, moves)
