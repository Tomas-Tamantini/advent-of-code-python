from dataclasses import dataclass
from typing import Hashable


@dataclass(frozen=True)
class StorageNode:
    id: Hashable
    size: int
    used: int

    @property
    def available(self) -> int:
        return self.size - self.used

    def makes_viable_pair(self, other: "StorageNode") -> bool:
        return self.used > 0 and self.id != other.id and self.used <= other.available
