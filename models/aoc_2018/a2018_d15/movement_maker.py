from typing import Optional, Iterator
from models.vectors import Vector2D, CardinalDirection
from models.graphs import explore_with_bfs
from .cave_map import CaveMap, CaveTile
from .units import CaveGameUnit
from .game_state import CaveGameState


class _Node:
    def __init__(
        self,
        position: Vector2D,
        parent: Optional["_Node"],
        incoming_direction: Optional[CardinalDirection],
    ) -> None:
        self.position = position
        self.parent = parent
        self.incoming_direction = incoming_direction

    def __hash__(self) -> int:
        return hash(self.position)

    def __eq__(self, other: object) -> bool:
        return self.position == other.position


class _Graph:
    def __init__(self, game_state: CaveGameState, cave_map: CaveMap) -> None:
        self._occupied_positions = {
            c.position for c in (game_state.elves + game_state.goblins)
        }
        self._cave_map = cave_map

    def is_valid_position(self, position: Vector2D) -> bool:
        return (
            position not in self._occupied_positions
            and self._cave_map.get_tile(position.x, position.y) != CaveTile.WALL
        )

    def neighbors(self, node: _Node) -> Iterator[_Node]:
        for direction in CardinalDirection.reading_order():
            mirrored_direction = (
                direction if direction.is_horizontal else direction.reverse()
            )
            new_pos = node.position.move(mirrored_direction)
            if self.is_valid_position(new_pos):
                yield _Node(new_pos, node, direction)


def move_direction(
    unit: CaveGameUnit, game_state: CaveGameState, cave_map: CaveMap
) -> Optional[CardinalDirection]:
    graph = _Graph(game_state, cave_map)
    target_positions = {
        p for p in game_state.target_positions(unit) if graph.is_valid_position(p)
    }
    if not target_positions:
        return None

    initial_node = _Node(unit.position, None, None)
    for node, _ in explore_with_bfs(graph, initial_node):
        if node.position in target_positions:
            while node.parent is not initial_node:
                node = node.parent
            return node.incoming_direction
    return None
