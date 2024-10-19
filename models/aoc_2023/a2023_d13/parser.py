from typing import Iterator, Iterable
from models.common.io import InputReader, CharacterGrid
from .logic import AshValley


def _contiguous_lines(lines: Iterable[str]) -> Iterator[str]:
    current_str = ""
    for line in lines:
        if line:
            current_str += "\n" + line
        else:
            if current_str:
                yield current_str
                current_str = ""
    if current_str:
        yield current_str


def parse_ash_valleys(input_reader: InputReader) -> Iterator[AshValley]:
    lines = list(input_reader.read_stripped_lines(keep_empty_lines=True))
    for contiguous in _contiguous_lines(lines):
        grid = CharacterGrid(contiguous)
        yield AshValley(grid)
