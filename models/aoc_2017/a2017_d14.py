from .a2017_d10 import knot_hash


class DiskGrid:
    def __init__(self, key: str, num_rows: int) -> None:
        self._key = key
        self._rows = [self._get_row_hash(row_num) for row_num in range(num_rows)]

    def get_row(self, row_num: int) -> str:
        return self._rows[row_num]

    def num_used_squares(self) -> int:
        return sum(row.count("1") for row in self._rows)

    def _get_row_hash(self, row_idx: int) -> str:
        hash_input = f"{self._key}-{row_idx}"
        hashed_lst = knot_hash(hash_input)
        return "".join(bin(num)[2:].zfill(8) for num in hashed_lst)
