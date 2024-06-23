from models.common.io import IOHandler
from .parser import parse_code_row_and_col


def row_and_col_to_index(row: int, col: int) -> int:
    diagonal_idx = row + col - 1
    return diagonal_idx * (diagonal_idx - 1) // 2 + col


def code_at(row: int, col: int, first_code: int, multiplier: int, mod: int) -> int:
    code = first_code
    for _ in range(1, row_and_col_to_index(row, col)):
        code = (code * multiplier) % mod
    return code


def aoc_2015_d25(io_handler: IOHandler) -> None:
    print("--- AOC 2015 - Day 25: Let It Snow ---")
    row_and_col = parse_code_row_and_col(io_handler.input_reader)
    code = code_at(**row_and_col, first_code=20151125, multiplier=252533, mod=33554393)
    print(f"Code at row {row_and_col['row']}, column {row_and_col['col']} is {code}")
