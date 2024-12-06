from math import inf
from queue import PriorityQueue
from typing import Iterator

from models.common.vectors import Vector2D

from .tunnel_maze_explorers import ExplorerMove, TunnelMazeExplorers
from .tunnel_maze_graph import TunnelMazeGraph


class TunnelMaze:
    def __init__(self) -> None:
        self._entrances: set[Vector2D] = set()
        self._keys: dict[str, Vector2D] = dict()
        self._doors: dict[str, Vector2D] = dict()
        self._graph = TunnelMazeGraph()

    def add_entrance(self, position: Vector2D) -> None:
        self._entrances.add(position)
        self._graph.add_node_and_connect_to_neighbors(position)

    def add_key(self, position: Vector2D, key_id: str) -> None:
        self._keys[key_id] = position
        self._graph.add_node_and_connect_to_neighbors(position)

    def add_door(self, position: Vector2D, corresponding_key_id: str) -> None:
        self._doors[corresponding_key_id] = position
        self._graph.add_node_and_connect_to_neighbors(position)

    def add_open_passage(self, position: Vector2D) -> None:
        self._graph.add_node_and_connect_to_neighbors(position)

    def reduced_graph(self) -> TunnelMazeGraph:
        irreducible_nodes = set()
        for entrance_position in self._entrances:
            irreducible_nodes.add(entrance_position)
        for key_position in self._keys.values():
            irreducible_nodes.add(key_position)
        for door_position in self._doors.values():
            irreducible_nodes.add(door_position)
        self._graph.reduce(irreducible_nodes)
        return self._graph

    def initial_explorers(self) -> TunnelMazeExplorers:
        positions = tuple(self._entrances)
        return TunnelMazeExplorers(positions=positions)

    def _collected_all_keys(self, explorer: TunnelMazeExplorers) -> bool:
        return len(explorer.collected_keys) == len(self._keys)

    def _locked_doors(self, explorer: TunnelMazeExplorers) -> Iterator[Vector2D]:
        for door_id, door_position in self._doors.items():
            if door_id not in explorer.collected_keys:
                yield door_position

    def _uncollected_keys(
        self, explorer: TunnelMazeExplorers
    ) -> Iterator[tuple[str, Vector2D]]:
        for key_id, key_position in self._keys.items():
            if key_id not in explorer.collected_keys:
                yield key_id, key_position

    def _forbidden_nodes(
        self, explorer: TunnelMazeExplorers, next_key: str
    ) -> Iterator[Vector2D]:
        for key_id, pos in self._uncollected_keys(explorer):
            if key_id != next_key:
                yield pos
        yield from self._locked_doors(explorer)

    def _available_moves(
        self, explorers: TunnelMazeExplorers
    ) -> Iterator[ExplorerMove]:
        for explorer_idx, explorer_position in enumerate(explorers.positions):
            for key_id, key_position in self._keys.items():
                if key_id not in explorers.collected_keys:
                    distance = self._graph.shortest_distance(
                        explorer_position,
                        key_position,
                        forbidden_nodes=set(
                            self._forbidden_nodes(explorers, next_key=key_id)
                        ),
                    )
                    if distance != inf:
                        yield ExplorerMove(explorer_idx, key_id, key_position, distance)

    def shortest_distance_to_all_keys(self) -> int:
        self._graph = self.reduced_graph()
        best_distance = inf
        queue = PriorityQueue()
        initial_explorers = self.initial_explorers()
        queue.put(initial_explorers)
        visited_states = set()
        while not queue.empty():
            explorers = queue.get()
            state = explorers.state()
            if state in visited_states or explorers.distance_walked >= best_distance:
                continue
            visited_states.add(state)
            if self._collected_all_keys(explorers):
                best_distance = explorers.distance_walked
                continue
            for move in self._available_moves(explorers):
                new_explorer = explorers.move_to_key(move)
                queue.put(new_explorer)
        return best_distance
