from typing import Iterator, Hashable
from dataclasses import dataclass


@dataclass(frozen=True)
class _MemoryBank:
    index: int
    num_blocks: int


class MemoryBankBalancer:
    def __init__(self, num_blocks: list[int]) -> None:
        self._num_blocks = num_blocks
        self._configurations = []
        self._loop_size = -1
        self._redistribution_cycle()

    def _largest_bank(self) -> _MemoryBank:
        max_num_blocks = max(self._num_blocks)
        return _MemoryBank(
            index=self._num_blocks.index(max_num_blocks),
            num_blocks=max_num_blocks,
        )

    def loop_size(self) -> int:
        return self._loop_size

    def _redistribute(self) -> None:
        largest_bank = self._largest_bank()
        self._num_blocks[largest_bank.index] = 0
        blocks_per_position = largest_bank.num_blocks // len(self._num_blocks)
        leftover_blocks = largest_bank.num_blocks % len(self._num_blocks)
        for i in range(len(self._num_blocks)):
            idx = (i + largest_bank.index + 1) % len(self._num_blocks)
            self._num_blocks[idx] += blocks_per_position
            if leftover_blocks > 0:
                self._num_blocks[idx] += 1
                leftover_blocks -= 1

    @property
    def _block_hashable(self) -> Hashable:
        return tuple(self._num_blocks)

    def _redistribution_cycle(self) -> None:
        visited = set()
        while True:
            self._configurations.append(self._block_hashable)
            visited.add(self._block_hashable)
            self._redistribute()
            if self._block_hashable in visited:
                self._loop_size = len(
                    self._configurations
                ) - self._configurations.index(self._block_hashable)
                break

    def unique_configurations(self) -> Iterator[tuple[int, ...]]:
        yield from self._configurations
