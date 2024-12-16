from collections import defaultdict
from math import inf
from typing import Iterable, Iterator, Optional

from models.common.graphs import GridMaze, WeightedUndirectedGraph, a_star
from models.common.vectors import CardinalDirection, Vector2D

from .reindeer_path_state import PathState
from .reindeer_racer import ReindeerRacer


class ReindeerMaze:
    def __init__(
        self,
        start_tile: Vector2D,
        start_direction: CardinalDirection,
        end_tile: Vector2D,
        maze_tiles: set[Vector2D],
    ):
        self._start_state = ReindeerRacer(start_tile, start_direction)
        self._end_tile = end_tile
        self._maze = self._build_maze(maze_tiles)
        self._cached_minimal_score = None
        self._move_forward_cost = 1
        self._turn_cost = 1000

    def _build_maze(self, maze_tiles: set[Vector2D]) -> WeightedUndirectedGraph:
        maze = GridMaze()
        for tile in maze_tiles:
            maze.add_node_and_connect_to_neighbors(tile)
        maze.reduce(set(self._irreducible_tiles(maze_tiles)))
        return maze

    @staticmethod
    def _corner_tiles(maze_tiles: set[Vector2D]) -> Iterator[Vector2D]:
        for tile in maze_tiles:
            neighbors = [n for n in tile.adjacent_positions() if n in maze_tiles]
            if len(neighbors) > 2:
                yield tile
            elif len(neighbors) == 2:
                delta_1 = neighbors[0] - tile
                delta_2 = neighbors[1] - tile
                if delta_1.dot_product(delta_2) == 0:
                    yield tile

    def _irreducible_tiles(self, maze_tiles: set[Vector2D]) -> Iterator[Vector2D]:
        yield self._start_state.position
        yield self._end_tile
        yield from self._corner_tiles(maze_tiles)

    def _is_final_state(self, state: ReindeerRacer) -> bool:
        return state.position == self._end_tile

    def _move_forward_neighbor(self, node: ReindeerRacer) -> Optional[Vector2D]:
        for neighbor in self._maze.neighbors(node.position):
            diff = neighbor.manhattan_distance(node.position)
            if (
                node.position.move(node.direction, num_steps=diff, y_grows_down=True)
                == neighbor
            ):
                return neighbor

    def neighbors(self, node: ReindeerRacer) -> Iterator[ReindeerRacer]:
        if (forward_tile := self._move_forward_neighbor(node)) is not None:
            yield ReindeerRacer(forward_tile, node.direction)
        yield node.turn_left()
        yield node.turn_right()

    def weight(self, node_a: ReindeerRacer, node_b: ReindeerRacer) -> float:
        if node_a.direction == node_b.direction:
            return self._move_forward_cost * self._maze.weight(
                node_a.position, node_b.position
            )
        else:
            return self._turn_cost

    def heuristic_potential(self, node: ReindeerRacer) -> float:
        return node.position.manhattan_distance(self._end_tile)

    def minimal_score(self) -> int:
        if self._cached_minimal_score is None:
            _, self._cached_minimal_score = a_star(
                origin=self._start_state,
                is_destination=self._is_final_state,
                graph=self,
            )
        return self._cached_minimal_score

    def _optimal_path_tiles(
        self, path_state: PathState, came_from: dict[PathState, Iterable[PathState]]
    ) -> Iterator[Vector2D]:
        for parent in came_from[path_state]:
            yield from path_state.positions_between(parent)
            yield from self._optimal_path_tiles(parent, came_from)

    def _neighboring_path_states(self, state: PathState) -> Iterator[PathState]:
        for neighbor in self.neighbors(state.racer):
            weight_increment = self.weight(state.racer, neighbor)
            yield PathState(
                neighbor, accumulated_cost=state.accumulated_cost + weight_increment
            )

    def tiles_on_optimal_paths(self) -> Iterator[Vector2D]:
        min_score_per_racer = dict()
        explore_stack = [PathState(self._start_state)]
        came_from = defaultdict(set)
        optimal_paths = set()
        while explore_stack:
            current_state = explore_stack.pop()
            if self._path_may_be_optimal(current_state, min_score_per_racer):
                min_score_per_racer[current_state.racer] = (
                    current_state.accumulated_cost
                )
                if current_state.racer.position == self._end_tile:
                    optimal_paths.add(current_state)
                else:
                    for neighbor in self._neighboring_path_states(current_state):
                        explore_stack.append(neighbor)
                        came_from[neighbor].add(current_state)

        for path_state in optimal_paths:
            yield from self._optimal_path_tiles(path_state, came_from)

    def _path_may_be_optimal(
        self, state: PathState, min_score_per_racer: dict[PathState, int]
    ) -> bool:
        return (
            state.accumulated_cost < min_score_per_racer.get(state.racer, inf)
            and state.cost_lower_bound(
                self._end_tile, self._move_forward_cost, self._turn_cost
            )
            <= self.minimal_score()
        )
