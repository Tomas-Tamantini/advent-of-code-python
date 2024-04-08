from dataclasses import dataclass, field
from models.vectors import Vector2D


@dataclass
class TunnelMazeExplorers:
    positions: tuple[Vector2D, ...]
    collected_keys: set[str] = field(default_factory=set)
    distance_walked: int = 0

    def __lt__(self, other):
        return self.distance_walked < other.distance_walked

    def state(self):
        return self.positions, tuple(sorted(self.collected_keys))

    def move_to_key(self, key_id: str, key_position: Vector2D, distance: int):
        new_positions = list(self.positions)
        new_positions[0] = key_position
        return TunnelMazeExplorers(
            positions=tuple(new_positions),
            collected_keys=self.collected_keys.union({key_id}),
            distance_walked=self.distance_walked + distance,
        )
