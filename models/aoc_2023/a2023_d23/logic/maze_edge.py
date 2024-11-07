from dataclasses import dataclass
from typing import Hashable


@dataclass(frozen=True)
class MazeEdge:
    node_a: Hashable
    node_b: Hashable
    weight: int
