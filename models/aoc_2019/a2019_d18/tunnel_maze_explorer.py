from dataclasses import dataclass, field
from models.vectors import Vector2D


@dataclass
class TunnelMazeExplorer:
    position: Vector2D
    collected_keys: set[str] = field(default_factory=set)
    distance_walked: int = 0

    def __lt__(self, other):
        return self.distance_walked < other.distance_walked

    def state(self):
        return self.position, tuple(sorted(self.collected_keys))

    def move_to_key(self, key_id: str, key_position: Vector2D, distance: int):
        return TunnelMazeExplorer(
            position=key_position,
            collected_keys=self.collected_keys.union({key_id}),
            distance_walked=self.distance_walked + distance,
        )
