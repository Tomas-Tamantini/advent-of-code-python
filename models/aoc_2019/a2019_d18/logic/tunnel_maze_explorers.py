from dataclasses import dataclass, field
from typing import Hashable

from models.common.vectors import Vector2D


@dataclass(frozen=True)
class ExplorerMove:
    explorer_idx: int
    key_id: str
    key_position: Vector2D
    distance: int


@dataclass
class TunnelMazeExplorers:
    positions: tuple[Vector2D, ...]
    collected_keys: set[str] = field(default_factory=set)
    distance_walked: int = 0

    def __lt__(self, other: "TunnelMazeExplorers") -> bool:
        return self.distance_walked < other.distance_walked

    def state(self) -> Hashable:
        return self.positions, tuple(sorted(self.collected_keys))

    def move_to_key(self, move: ExplorerMove) -> "TunnelMazeExplorers":
        new_positions = list(self.positions)
        new_positions[move.explorer_idx] = move.key_position
        return TunnelMazeExplorers(
            positions=tuple(new_positions),
            collected_keys=self.collected_keys.union({move.key_id}),
            distance_walked=self.distance_walked + move.distance,
        )
