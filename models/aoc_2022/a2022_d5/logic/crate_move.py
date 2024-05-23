from dataclasses import dataclass
from .crate import Crate


@dataclass(frozen=True)
class MoveCratesOneAtATime:
    origin_id: int
    destination_id: int
    num_times: int

    def apply(self, crates: dict[int, Crate]) -> None:
        for _ in range(self.num_times):
            crates[self.destination_id].push(crates[self.origin_id].pop())


@dataclass
class MoveCratesMultipleAtATime:
    origin_id: int
    destination_id: int
    num_times: int

    def apply(self, crates: dict[int, Crate]) -> None:
        intermediate_stack = []
        for _ in range(self.num_times):
            intermediate_stack.append(crates[self.origin_id].pop())
        for item in reversed(intermediate_stack):
            crates[self.destination_id].push(item)
