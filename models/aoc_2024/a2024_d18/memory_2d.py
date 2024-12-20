from math import ceil, log2
from typing import Iterator

from models.common.graphs import min_path_length_with_bfs
from models.common.io import ProgressBar
from models.common.vectors import Vector2D


class Memory2D:
    def __init__(self, width: int, height: int, corrupted_positions: list[Vector2D]):
        self._width = width
        self._height = height
        self._corrupted_positions = corrupted_positions
        self._end_position = None

    def _is_within_bounds(self, pos: Vector2D) -> bool:
        return 0 <= pos.x < self._width and 0 <= pos.y < self._height

    def neighbors(self, node: Vector2D) -> Iterator[Vector2D]:
        for pos in node.adjacent_positions():
            if self._is_within_bounds(pos) and (pos not in self._corrupted_positions):
                yield pos

    def shortest_path(self, start: Vector2D, end: Vector2D) -> int:
        self._end_position = end
        try:
            return min_path_length_with_bfs(self, start, lambda p: p == end)
        except ValueError:
            return -1


def index_of_first_blocking_byte(
    memory_size: tuple[int, int],
    corrupted_positions: list[Vector2D],
    lb: int = 0,
    ub: int | None = None,
    progress_bar: ProgressBar | None = None,
) -> int:
    start = Vector2D(0, 0)
    end = Vector2D(memory_size[0] - 1, memory_size[1] - 1)
    if ub is None:
        ub = len(corrupted_positions)
    expected_num_steps = ceil(log2(ub - lb))
    while lb < ub:
        mid = (lb + ub) // 2
        if progress_bar:
            current_step = expected_num_steps - ceil(log2(ub - lb))
            progress_bar.update(current_step, expected_num_steps)
        memory = Memory2D(*memory_size, corrupted_positions=corrupted_positions[:mid])
        if memory.shortest_path(start, end) != -1:
            lb = mid + 1
        else:
            ub = mid

    return lb - 1
