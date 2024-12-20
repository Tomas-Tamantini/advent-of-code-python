from dataclasses import dataclass
from itertools import combinations
from typing import Iterator

from models.common.graphs import explore_with_bfs, min_path_length_with_bfs
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

    def _cheat_positions(self) -> Iterator[tuple[Vector2D, Vector2D]]:
        for start_pos, end_pos in combinations(self._track_positions, 2):
            distance = start_pos.manhattan_distance(end_pos)
            if distance <= 2:
                yield start_pos, end_pos
                yield end_pos, start_pos

    def advantageous_cheats(self) -> Iterator[_Cheat]:
        _distance_to_start = dict()
        for node, distance in explore_with_bfs(self, self._start):
            _distance_to_start[node] = distance
        _distance_to_end = dict()
        for node, distance in explore_with_bfs(self, self._end):
            _distance_to_end[node] = distance
        min_time_without_cheat = self._min_time_without_cheat()
        cheat_positions = list(self._cheat_positions())
        for cheat_start, cheat_end in cheat_positions:
            cheat_time = (
                _distance_to_start[cheat_start]
                + cheat_start.manhattan_distance(cheat_end)
                + _distance_to_end[cheat_end]
            )
            if cheat_time < min_time_without_cheat:
                yield _Cheat(
                    cheat_start, cheat_end, min_time_without_cheat - cheat_time
                )
