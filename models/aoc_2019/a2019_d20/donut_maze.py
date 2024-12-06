from dataclasses import dataclass
from math import inf
from typing import Iterator

from models.common.graphs import GridMaze, dijkstra
from models.common.vectors import Vector2D


class PortalMaze(GridMaze):
    def __init__(self) -> None:
        super().__init__()
        self._entrance = None
        self._exit = None

    def set_entrance(self, entrance: Vector2D) -> None:
        self._entrance = entrance

    def set_exit(self, exit: Vector2D) -> None:
        self._exit = exit

    def add_portal(self, portal_a: Vector2D, portal_b: Vector2D) -> None:
        self._try_add_edge(portal_a, portal_b, 1)

    def num_steps_to_solve(self) -> int:
        self.reduce(irreducible_nodes={self._entrance, self._exit})
        return self.shortest_distance(self._entrance, self._exit)


@dataclass(frozen=True)
class DonutMazeNode:
    position: Vector2D
    level: int


class RecursiveDonutMaze:
    def __init__(self) -> None:
        self._main_maze = GridMaze()
        self._entrance = None
        self._exit = None
        self._step_up_to_step_down_portals = {}
        self._step_down_to_step_up_portals = {}

    def add_node(self, node: Vector2D) -> None:
        self._main_maze.add_node_and_connect_to_neighbors(node)

    def set_entrance(self, entrance: Vector2D) -> None:
        self._entrance = entrance

    def set_exit(self, exit: Vector2D) -> None:
        self._exit = exit

    def add_portal(self, step_up: Vector2D, step_down: Vector2D) -> None:
        self._step_up_to_step_down_portals[step_up] = step_down
        self._step_down_to_step_up_portals[step_down] = step_up

    def irreducible_nodes(self) -> Iterator[Vector2D]:
        yield self._entrance
        yield self._exit
        yield from self._step_up_to_step_down_portals.keys()
        yield from self._step_down_to_step_up_portals.keys()

    def neighbors(self, node: DonutMazeNode) -> Iterator[DonutMazeNode]:
        for neighboring_position in self._main_maze.neighbors(node.position):
            yield DonutMazeNode(neighboring_position, node.level)

        if node.position in self._step_up_to_step_down_portals:
            step_down = self._step_up_to_step_down_portals[node.position]
            yield DonutMazeNode(step_down, node.level + 1)

        if node.position in self._step_down_to_step_up_portals and node.level > 0:
            step_up = self._step_down_to_step_up_portals[node.position]
            yield DonutMazeNode(step_up, node.level - 1)

    def _are_neighbors_from_different_levels(
        self, node_a: DonutMazeNode, node_b: DonutMazeNode
    ) -> bool:
        return (
            node_a.level == node_b.level - 1
            and node_a.position
            == self._step_down_to_step_up_portals.get(node_b.position, None)
        ) or (
            node_a.level == node_b.level + 1
            and node_a.position
            == self._step_up_to_step_down_portals.get(node_b.position, None)
        )

    def weight(self, node_a: DonutMazeNode, node_b: DonutMazeNode) -> float:
        if node_a.level == node_b.level:
            return self._main_maze.weight(node_a.position, node_b.position)
        return 1 if self._are_neighbors_from_different_levels(node_a, node_b) else inf

    def num_steps_to_solve(self) -> int:
        self._main_maze.reduce(irreducible_nodes=set(self.irreducible_nodes()))
        origin = DonutMazeNode(self._entrance, level=0)
        destination = DonutMazeNode(self._exit, level=0)
        try:
            return dijkstra(origin, destination, self)[1]
        except ValueError:
            return inf
