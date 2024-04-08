from dataclasses import dataclass, field
from models.vectors import Vector2D


@dataclass
class TunnelMazeExplorer:
    position: Vector2D
    collected_keys: set[str] = field(default_factory=set)
    distance_walked: int = 0
