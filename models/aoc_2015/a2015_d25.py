def row_and_col_to_index(row: int, col: int) -> int:
    diagonal_idx = row + col - 1
    return diagonal_idx * (diagonal_idx - 1) // 2 + col


def code_at(row: int, col: int, first_code: int, multiplier: int, mod: int) -> int:
    code = first_code
    for _ in range(1, row_and_col_to_index(row, col)):
        code = (code * multiplier) % mod
    return code
