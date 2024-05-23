from dataclasses import dataclass
from .crate import Crate


@dataclass(frozen=True)
class MoveCrateItems:
    origin_id: int
    destination_id: int
    num_times: int

    def apply(self, crates: dict[int, Crate]) -> None:
        for _ in range(self.num_times):
            crates[self.destination_id].push(crates[self.origin_id].pop())
