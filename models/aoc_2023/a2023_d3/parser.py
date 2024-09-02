from typing import Iterator
from models.common.io import InputReader
from .logic import EngineSymbol, PartNumber


def parse_engine_symbols(input_reader: InputReader) -> Iterator[EngineSymbol]:
    for row, line in enumerate(input_reader.read_stripped_lines()):
        for col, symbol_chr in enumerate(line):
            if not symbol_chr.isdigit() and symbol_chr != ".":
                yield EngineSymbol(symbol_chr=symbol_chr, row=row, column=col)


def parse_part_numbers(input_reader: InputReader) -> Iterator[PartNumber]:
    for row, line in enumerate(input_reader.read_stripped_lines()):
        current_number = ""
        for col, symbol_chr in enumerate(line):
            if symbol_chr.isdigit():
                current_number += symbol_chr
            elif current_number:
                yield PartNumber(
                    serial=current_number,
                    row=row,
                    start_column=col - len(current_number),
                )
                current_number = ""
        if current_number:
            yield PartNumber(
                serial=current_number,
                row=row,
                start_column=len(line) - len(current_number),
            )
            current_number = ""
