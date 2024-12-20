from dataclasses import dataclass
from typing import Iterator

from models.common.graphs import min_path_length_with_bfs
from models.common.vectors import Vector2D, CardinalDirection


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
        self._cheat_position = None

    def neighbors(self, node: Vector2D) -> Iterator[Vector2D]:
        if node != self._end:
            for neighbor in node.adjacent_positions():
                if neighbor in self._track_positions or (
                    self._cheat_position and neighbor == self._cheat_position[0]
                ):
                    yield neighbor

    def _min_time(self) -> int:
        return min_path_length_with_bfs(
            self, self._start, is_final_state=lambda pos: pos == self._end
        )

    def _cheat_positions(self) -> Iterator[tuple[Vector2D, Vector2D]]:
        for pos in self._track_positions:
            for direction in {CardinalDirection.EAST, CardinalDirection.SOUTH}:
                start_pos = pos.move(direction)
                if start_pos in self._wall_positions:
                    end_pos = start_pos.move(direction)
                    if end_pos in self._track_positions:
                        yield start_pos, end_pos

    def advantageous_cheats(self, min_saved_time: int) -> Iterator[_Cheat]:
        self._cheat_position = None
        time_without_cheat = self._min_time()
        max_time_with_cheat = time_without_cheat - min_saved_time
        cheat_positions = list(self._cheat_positions())
        for i, cheat_pos in enumerate(cheat_positions):
            self._cheat_position = cheat_pos
            cheat_time = self._min_time()
            if cheat_time <= max_time_with_cheat:
                yield _Cheat(*cheat_pos, saved_time=time_without_cheat - cheat_time)
