from dataclasses import dataclass
from typing import Iterator

from models.common.graphs import explore_with_bfs, min_path_length_with_bfs
from models.common.io import ProgressBar
from models.common.vectors import Vector2D


@dataclass(frozen=True)
class _Cheat:
    start_pos: Vector2D
    end_pos: Vector2D
    saved_time: int


class CpuRacetrack:
    def __init__(
        self,
        start: Vector2D,
        end: Vector2D,
        track_positions: set[Vector2D],
        wall_positions: set[Vector2D],
    ):
        self._start = start
        self._end = end
        self._track_positions = track_positions
        self._wall_positions = wall_positions

    def neighbors(self, node: Vector2D) -> Iterator[Vector2D]:
        for neighbor in node.adjacent_positions():
            if neighbor in self._track_positions:
                yield neighbor

    def _min_time_without_cheat(self) -> int:
        return min_path_length_with_bfs(self, self._start, lambda p: p == self._end)

    def _cheat_end_positions(
        self, start_pos: Vector2D, cheat_length: int
    ) -> Iterator[Vector2D]:
        for x_offset in range(cheat_length + 1):
            if x_offset == 0:
                min_y, max_y = 0, cheat_length
            else:
                max_y = cheat_length - x_offset
                min_y = -max_y
            for y_offset in range(min_y, max_y + 1):
                end_pos = start_pos + Vector2D(x_offset, y_offset)
                if (
                    end_pos in self._track_positions
                    and start_pos.manhattan_distance(end_pos) <= cheat_length
                ):
                    yield end_pos

    def _cheat_positions(
        self, cheat_length: int, progress_bar: ProgressBar | None
    ) -> Iterator[tuple[Vector2D, Vector2D]]:
        for i, start_pos in enumerate(self._track_positions):
            if progress_bar:
                progress_bar.update(i, len(self._track_positions))
            for end_pos in self._cheat_end_positions(start_pos, cheat_length):
                yield start_pos, end_pos
                yield end_pos, start_pos

    def advantageous_cheats(
        self, cheat_length: int, progress_bar: ProgressBar | None = None
    ) -> Iterator[_Cheat]:
        _distance_to_start = dict()
        for node, distance in explore_with_bfs(self, self._start):
            _distance_to_start[node] = distance
        _distance_to_end = dict()
        for node, distance in explore_with_bfs(self, self._end):
            _distance_to_end[node] = distance
        min_time_without_cheat = self._min_time_without_cheat()
        for cheat_start, cheat_end in self._cheat_positions(cheat_length, progress_bar):
            cheat_time = (
                _distance_to_start[cheat_start]
                + cheat_start.manhattan_distance(cheat_end)
                + _distance_to_end[cheat_end]
            )
            if cheat_time < min_time_without_cheat:
                yield _Cheat(
                    cheat_start, cheat_end, min_time_without_cheat - cheat_time
                )
