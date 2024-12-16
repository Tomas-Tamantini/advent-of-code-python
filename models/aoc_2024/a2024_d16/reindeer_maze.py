from dataclasses import dataclass
from typing import Iterator

from models.common.graphs import a_star
from models.common.vectors import CardinalDirection, Vector2D


@dataclass(frozen=True)
class _ReindeerRacer:
    position: Vector2D
    direction: CardinalDirection

    def move_forward(self) -> "_ReindeerRacer":
        return _ReindeerRacer(
            self.position.move(self.direction, y_grows_down=True), self.direction
        )

    def turn_left(self) -> "_ReindeerRacer":
        return _ReindeerRacer(self.position, self.direction.turn_left())

    def turn_right(self) -> "_ReindeerRacer":
        return _ReindeerRacer(self.position, self.direction.turn_right())


class ReindeerMaze:
    def __init__(
        self,
        start_tile: Vector2D,
        start_direction: CardinalDirection,
        end_tile: Vector2D,
        maze_tiles: set[Vector2D],
    ):
        self._start_state = _ReindeerRacer(start_tile, start_direction)
        self._end_tile = end_tile
        self._maze_tiles = maze_tiles

    def _is_final_state(self, state: _ReindeerRacer) -> bool:
        return state.position == self._end_tile

    def neighbors(self, node: _ReindeerRacer) -> Iterator[_ReindeerRacer]:
        new_state = node.move_forward()
        if new_state.position in self._maze_tiles:
            yield new_state
        yield node.turn_left()
        yield node.turn_right()

    @staticmethod
    def weight(node_a: _ReindeerRacer, node_b: _ReindeerRacer) -> float:
        if node_a.direction == node_b.direction:
            return node_a.position.manhattan_distance(node_b.position)
        else:
            return 1000

    def heuristic_potential(self, node: _ReindeerRacer) -> float:
        return node.position.manhattan_distance(self._end_tile)

    def minimal_score(self) -> int:
        return a_star(
            origin=self._start_state, is_destination=self._is_final_state, graph=self
        )[1]
