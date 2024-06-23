from io import StringIO
import numpy as np
from models.common.io import IOHandler
from .spreadsheet import Spreadsheet


def aoc_2017_d2(io_handler: IOHandler) -> None:
    print("--- AOC 2017 - Day 2: Corruption Checksum ---")
    string_io = StringIO(io_handler.input_reader.read())
    spreadsheet = Spreadsheet(np.loadtxt(string_io, dtype=int, delimiter="\t"))
    print(f"Part 1: Spreadsheet checksum min/max: {spreadsheet.checksum_min_max()}")
    print(
        f"Part 2: Spreadsheet checksum divisibility: {spreadsheet.checksum_divisibility()}"
    )
