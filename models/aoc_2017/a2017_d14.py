from .a2017_d10 import knot_hash
from models.common.vectors import Vector2D
from models.common.graphs import explore_with_bfs


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

    def _is_valid_pos(self, pos: Vector2D) -> bool:
        return (
            0 <= pos.x < len(self._rows)
            and 0 <= pos.y < len(self._rows[0])
            and self._rows[pos.x][pos.y] == "1"
        )

    def neighbors(self, pos: Vector2D) -> Vector2D:
        for new_pos in pos.adjacent_positions():
            if self._is_valid_pos(new_pos):
                yield new_pos

    def num_regions(self) -> int:
        num_regions = 0
        visited = set()
        for row_idx in range(len(self._rows)):
            for col_idx in range(len(self._rows[row_idx])):
                pos = Vector2D(row_idx, col_idx)
                if self._rows[row_idx][col_idx] == "1" and pos not in visited:
                    num_regions += 1
                    for new_pos, _ in explore_with_bfs(self, pos):
                        visited.add(new_pos)

        return num_regions
