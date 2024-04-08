from queue import PriorityQueue
from math import inf
from typing import Iterator
from models.vectors import Vector2D
from .tunnel_maze_graph import TunnelMazeGraph
from .tunnel_maze_explorer import TunnelMazeExplorer


class TunnelMaze:
    def __init__(self) -> None:
        self._entrance: Vector2D = None
        self._keys: dict[str, Vector2D] = dict()
        self._doors: dict[str, Vector2D] = dict()
        self._graph = TunnelMazeGraph()

    def set_entrance(self, position: Vector2D) -> None:
        self._entrance = position
        self._graph.add_node(position)

    def add_key(self, position: Vector2D, key_id: str) -> None:
        self._keys[key_id] = position
        self._graph.add_node(position)

    def add_door(self, position: Vector2D, corresponding_key_id: str) -> None:
        self._doors[corresponding_key_id] = position
        self._graph.add_node(position)

    def add_open_passage(self, position: Vector2D) -> None:
        self._graph.add_node(position)

    def reduced_graph(self) -> TunnelMazeGraph:
        irreducible_nodes = set()
        irreducible_nodes.add(self._entrance)
        for key_position in self._keys.values():
            irreducible_nodes.add(key_position)
        for door_position in self._doors.values():
            irreducible_nodes.add(door_position)
        self._graph.reduce(irreducible_nodes)
        return self._graph

    def initial_explorer(self):
        return TunnelMazeExplorer(position=self._entrance)

    def _collected_all_keys(self, explorer: TunnelMazeExplorer) -> bool:
        return len(explorer.collected_keys) == len(self._keys)

    def _locked_doors(self, explorer: TunnelMazeExplorer) -> Iterator[Vector2D]:
        for door_id, door_position in self._doors.items():
            if door_id not in explorer.collected_keys:
                yield door_position

    def _uncollected_keys(
        self, explorer: TunnelMazeExplorer
    ) -> Iterator[tuple[str, Vector2D]]:
        for key_id, key_position in self._keys.items():
            if key_id not in explorer.collected_keys:
                yield key_id, key_position

    def _forbidden_nodes(
        self, explorer: TunnelMazeExplorer, next_key: str
    ) -> Iterator[Vector2D]:
        for key_id, pos in self._uncollected_keys(explorer):
            if key_id != next_key:
                yield pos
        yield from self._locked_doors(explorer)

    def _neighboring_keys(
        self, explorer: TunnelMazeExplorer
    ) -> Iterator[tuple[str, Vector2D, int]]:
        for key_id, key_position in self._keys.items():
            if key_id not in explorer.collected_keys:
                distance = self._graph.shortest_distance(
                    explorer.position,
                    key_position,
                    forbidden_nodes=set(
                        self._forbidden_nodes(explorer, next_key=key_id)
                    ),
                )
                if distance != inf:
                    yield key_id, key_position, distance

    def shortest_distance_to_all_keys(self) -> int:
        self._graph = self.reduced_graph()
        best_distance = inf
        queue = PriorityQueue()
        initial_explorer = self.initial_explorer()
        queue.put(initial_explorer)
        visited_states = set()
        while not queue.empty():
            explorer = queue.get()
            state = explorer.state()
            if state in visited_states or explorer.distance_walked >= best_distance:
                continue
            visited_states.add(state)
            if self._collected_all_keys(explorer):
                best_distance = explorer.distance_walked
                continue
            for key_id, key_position, distance in self._neighboring_keys(explorer):
                new_explorer = explorer.move_to_key(key_id, key_position, distance)
                queue.put(new_explorer)
        return best_distance
