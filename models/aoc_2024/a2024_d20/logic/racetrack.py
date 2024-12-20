from dataclasses import dataclass
from typing import Iterator

from models.common.graphs import explore_with_bfs, GridMaze
from models.common.vectors import Vector2D


@dataclass(frozen=True)
class _Cheat:
    start_pos: Vector2D
    end_pos: Vector2D
    saved_time: int


@dataclass(frozen=True)
class _RaceState:
    position: Vector2D
    cheat_start_pos: Vector2D | None
    cheat_end_pos: Vector2D | None


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

    def neighbors(self, node: _RaceState) -> Iterator[_RaceState]:
        if node.position != self._end:
            for neighbor_pos in node.position.adjacent_positions():
                if neighbor_pos in self._track_positions:
                    cheat_end = None if node.cheat_start_pos is None else neighbor_pos
                    yield _RaceState(neighbor_pos, node.cheat_start_pos, cheat_end)
                elif (
                    neighbor_pos in self._wall_positions
                ) and node.cheat_start_pos is None:
                    yield _RaceState(neighbor_pos, neighbor_pos, None)

    def _min_time_without_cheat(self) -> int:
        _maze = GridMaze()
        for node in self._track_positions:
            _maze.add_node_and_connect_to_neighbors(node)
        _maze.reduce(irreducible_nodes={self._start, self._end})
        return _maze.shortest_distance(self._start, self._end)

    def advantageous_cheats(self, min_saved_time: int) -> Iterator[_Cheat]:
        time_without_cheat = self._min_time_without_cheat()
        max_time_with_cheat = time_without_cheat - min_saved_time
        times_with_cheat = dict()
        initial_node = _RaceState(
            position=self._start, cheat_start_pos=None, cheat_end_pos=None
        )
        for node, time in explore_with_bfs(self, initial_node):
            if time > max_time_with_cheat:
                break
            if node.position == self._end:
                times_with_cheat[(node.cheat_start_pos, node.cheat_end_pos)] = time

        for cheat_pos, cheat_time in times_with_cheat.items():
            saved_time = time_without_cheat - cheat_time
            if saved_time > 0:
                yield _Cheat(*cheat_pos, saved_time)
