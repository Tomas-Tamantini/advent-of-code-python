from typing import Iterator
from models.common.io import InputReader
from .scratchcard import ScratchCard


def _parse_scratchcard(line: str) -> ScratchCard:
    card_id, numbers = line.split(":")
    card_id = int(card_id.split()[1])
    winning_numbers, chosen_numbers = numbers.split("|")
    winning_numbers = {int(num) for num in winning_numbers.split()}
    chosen_numbers = {int(num) for num in chosen_numbers.split()}
    return ScratchCard(card_id, winning_numbers, chosen_numbers)


def parse_scratchcards(input_reader: InputReader) -> Iterator[ScratchCard]:
    for line in input_reader.read_stripped_lines():
        yield _parse_scratchcard(line)
