from collections import defaultdict
from dataclasses import dataclass
from math import inf
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


@dataclass(frozen=True)
class _PathState:
    racer: _ReindeerRacer
    accumulated_cost: int = 0

    def cost_lower_bound(
        self, end_tile: Vector2D, move_forward_cost: int, turn_cost: int
    ) -> int:
        delta = end_tile - self.racer.position
        lb = self.accumulated_cost + move_forward_cost * delta.manhattan_size
        if delta.x == 0 or delta.y == 0:
            return lb
        else:
            return lb + turn_cost


def _positions_between(start: Vector2D, end: Vector2D) -> Iterator[Vector2D]:
    diff = end - start
    diff_size = diff.manhattan_size
    if diff_size == 0:
        yield start
    else:
        diff_normal = Vector2D(diff.x // diff_size, diff.y // diff_size)
        for i in range(diff_size + 1):
            yield start + i * diff_normal


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

    def tiles_on_optimal_paths(self) -> Iterator[Vector2D]:
        # TODO: Refactor
        min_score_per_racer = dict()
        min_score = self.minimal_score()
        explore_stack = [_PathState(self._start_state, accumulated_cost=0)]
        visited = set()
        came_from = defaultdict(set)
        optimal_paths = set()
        while explore_stack:
            current_path_state = explore_stack.pop()
            if (
                current_path_state in visited
                or current_path_state.accumulated_cost
                > min_score_per_racer.get(current_path_state.racer, inf)
                or current_path_state.cost_lower_bound(
                    self._end_tile, self._move_forward_cost, self._turn_cost
                )
                > min_score
            ):
                continue
            visited.add(current_path_state)
            min_score_per_racer[current_path_state.racer] = (
                current_path_state.accumulated_cost
            )
            if current_path_state.racer.position == self._end_tile:
                optimal_paths.add(current_path_state)
            else:
                for neighbor in self.neighbors(current_path_state.racer):
                    weight_increment = self.weight(current_path_state.racer, neighbor)
                    new_path_state = _PathState(
                        neighbor,
                        accumulated_cost=current_path_state.accumulated_cost
                        + weight_increment,
                    )
                    explore_stack.append(new_path_state)
                    came_from[new_path_state].add(current_path_state)
        for path_state in optimal_paths:
            yield_stack = [path_state]
            while yield_stack:
                current_path_state = yield_stack.pop()
                for parent in came_from[current_path_state]:
                    yield from _positions_between(
                        current_path_state.racer.position, parent.racer.position
                    )
                    yield_stack.append(parent)
