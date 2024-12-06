import numpy as np

from models.common.io import InputReader

from .bingo import BingoBoard, BingoGame


def parse_bingo_game_and_numbers_to_draw(
    input_reader: InputReader,
) -> tuple[BingoGame, list[int]]:
    lines = list(input_reader.read_stripped_lines(keep_empty_lines=True))
    tables = []
    numbers_to_draw = []
    current_table = []
    for line in lines:
        if "," in line:
            numbers_to_draw = list(map(int, line.split(",")))
        elif line:
            current_table.append(list(map(int, line.split())))
        elif current_table:
            tables.append(current_table)
            current_table = []
    if current_table:
        tables.append(current_table)
    boards = (BingoBoard(np.array(board, dtype=np.int32)) for board in tables)
    return BingoGame(tuple(boards)), numbers_to_draw
