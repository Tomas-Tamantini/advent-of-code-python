from dataclasses import dataclass
from collections import defaultdict
from typing import Protocol, Optional


@dataclass(frozen=True)
class Bitmask:
    mask: str

    def apply(self, value: int) -> int:
        return (value | int(self.mask.replace("X", "0"), base=2)) & int(
            self.mask.replace("X", "1"), base=2
        )


class BitmaskMemory:
    def __init__(self, mask: Optional[Bitmask] = None) -> None:
        self._mask = mask
        self._stored_values = defaultdict(int)

    def update_mask(self, mask: Bitmask) -> None:
        self._mask = mask

    def store(self, address: int, value: int) -> None:
        transformed_value = value if self._mask is None else self._mask.apply(value)
        self._stored_values[address] = transformed_value

    def sum_values(self) -> int:
        return sum(self._stored_values.values())


class BitmaskInstruction(Protocol):
    def execute(self, memory: BitmaskMemory) -> None: ...


@dataclass(frozen=True)
class SetMaskInstruction:
    mask: str

    def execute(self, memory: BitmaskMemory) -> None:
        memory.update_mask(Bitmask(self.mask))


@dataclass(frozen=True)
class WriteToMemoryInstruction:
    address: int
    value: int

    def execute(self, memory: BitmaskMemory) -> None:
        memory.store(self.address, self.value)
