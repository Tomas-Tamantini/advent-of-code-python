from dataclasses import dataclass
from models.vectors import Vector2D


@dataclass(frozen=True)
class NetworkPacket:
    destination_address: int
    content: Vector2D
