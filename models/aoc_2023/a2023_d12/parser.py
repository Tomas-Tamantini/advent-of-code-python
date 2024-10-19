from typing import Iterator
from models.common.io import InputReader
from .logic import NonogramRow


def _parse_nonogram_row(line: str, number_of_repetitions: int) -> NonogramRow:
    parts = line.split()
    cells = parts[0].strip()
    groups = list(eval(parts[1]))
    repeated_cells = "?".join([cells for _ in range(number_of_repetitions)])
    repeated_groups = tuple(groups * number_of_repetitions)
    return NonogramRow(repeated_cells, repeated_groups)


def parse_nonogram_rows(
    input_reader: InputReader, number_of_repetitions: int
) -> Iterator[NonogramRow]:
    for line in input_reader.read_stripped_lines():
        yield _parse_nonogram_row(line, number_of_repetitions)
