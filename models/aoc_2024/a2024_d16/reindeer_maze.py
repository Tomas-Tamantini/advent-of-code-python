from dataclasses import dataclass
from typing import Iterator, Optional

from models.common.graphs import GridMaze, a_star
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


class _ReindeerPath:
    def __init__(self, states: tuple[_ReindeerRacer, ...], weight: int):
        self._states = states
        self._weight = weight

    @staticmethod
    def _positions_between(
        position_before: _ReindeerRacer, position_after: _ReindeerRacer
    ) -> Iterator[Vector2D]:
        diff = position_after - position_before
        diff_size = diff.manhattan_size
        if diff_size > 0:
            diff_normal = Vector2D(diff.x // diff_size, diff.y // diff_size)
            for i in range(1, diff_size + 1):
                yield position_before + i * diff_normal

    def tiles(self) -> Iterator[Vector2D]:
        yield self._states[0].position
        for i in range(1, len(self._states)):
            pos_before = self._states[i - 1].position
            pos_after = self._states[i].position
            yield from self._positions_between(pos_before, pos_after)

    @property
    def last_state(self) -> _ReindeerRacer:
        return self._states[-1]

    def add_state(
        self, state: _ReindeerRacer, weight_increment: int
    ) -> "_ReindeerPath":
        return _ReindeerPath(
            states=self._states + (state,), weight=self._weight + weight_increment
        )

    def weight_lower_bound(
        self, end_tile: Vector2D, move_forward_cost: int, turn_cost: int
    ) -> int:
        delta = end_tile - self.last_state.position
        lb = self._weight + move_forward_cost * delta.manhattan_size
        if delta.x == 0 or delta.y == 0:
            return lb
        else:
            return lb + turn_cost


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
        self._maze = GridMaze()
        for tile in maze_tiles:
            self._maze.add_node_and_connect_to_neighbors(tile)
        self._maze.reduce(set(self._irreducible_tiles(maze_tiles)))
        # TODO: Make these parameters configurable
        self._move_forward_cost = 1
        self._turn_cost = 1000

    def _irreducible_tiles(self, maze_tiles: set[Vector2D]) -> Iterator[Vector2D]:
        yield self._start_state.position
        yield self._end_tile
        # Find corner tiles
        for tile in maze_tiles:
            neighbors = [n for n in tile.adjacent_positions() if n in maze_tiles]
            if len(neighbors) > 2:
                yield tile
            elif len(neighbors) == 2:
                delta_1 = neighbors[0] - tile
                delta_2 = neighbors[1] - tile
                if delta_1.dot_product(delta_2) == 0:
                    yield tile

    def _is_final_state(self, state: _ReindeerRacer) -> bool:
        return state.position == self._end_tile

    def _move_forward_neighbor(self, node: _ReindeerRacer) -> Optional[Vector2D]:
        for neighbor in self._maze.neighbors(node.position):
            diff = neighbor.manhattan_distance(node.position)
            if (
                node.position.move(node.direction, num_steps=diff, y_grows_down=True)
                == neighbor
            ):
                return neighbor

    def neighbors(self, node: _ReindeerRacer) -> Iterator[_ReindeerRacer]:
        if (forward_tile := self._move_forward_neighbor(node)) is not None:
            yield _ReindeerRacer(forward_tile, node.direction)
        yield node.turn_left()
        yield node.turn_right()

    def weight(self, node_a: _ReindeerRacer, node_b: _ReindeerRacer) -> float:
        if node_a.direction == node_b.direction:
            return self._move_forward_cost * node_a.position.manhattan_distance(
                node_b.position
            )
        else:
            return self._turn_cost

    def heuristic_potential(self, node: _ReindeerRacer) -> float:
        return node.position.manhattan_distance(self._end_tile)

    def minimal_score(self) -> int:
        return a_star(
            origin=self._start_state, is_destination=self._is_final_state, graph=self
        )[1]

    def _optimal_paths(self) -> Iterator[_ReindeerPath]:
        min_score = self.minimal_score()
        path = _ReindeerPath(states=(self._start_state,), weight=0)
        explore_stack = [path]
        while explore_stack:
            current_path = explore_stack.pop()
            if (
                current_path.weight_lower_bound(
                    self._end_tile, self._move_forward_cost, self._turn_cost
                )
                > min_score
            ):
                continue
            if current_path.last_state.position == self._end_tile:
                yield current_path
            else:
                for next_state in self.neighbors(current_path.last_state):
                    weight_increment = self.weight(current_path.last_state, next_state)
                    new_path = current_path.add_state(next_state, weight_increment)
                    explore_stack.append(new_path)

    def tiles_on_optimal_paths(self) -> Iterator[Vector2D]:
        for path in self._optimal_paths():
            yield from path.tiles()
