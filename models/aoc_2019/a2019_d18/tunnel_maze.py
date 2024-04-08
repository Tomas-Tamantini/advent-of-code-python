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

    def shortest_distance_to_all_keys(self) -> int:
        return 0
