from typing import Iterator, Iterable
from dataclasses import dataclass


@dataclass(frozen=True)
class _MemoryBank:
    index: int
    num_blocks: int


class MemoryBankBalancer:
    def __init__(self, num_blocks: list[int]) -> None:
        self._num_blocks = num_blocks

    @staticmethod
    def _largest_bank(num_blocks: Iterable[int]) -> _MemoryBank:
        max_num_blocks = max(num_blocks)
        return _MemoryBank(
            index=num_blocks.index(max_num_blocks),
            num_blocks=max_num_blocks,
        )

    def unique_configurations(self) -> Iterator[tuple[int, ...]]:
        num_blocks = self._num_blocks[:]
        yield tuple(self._num_blocks)
        visited = {tuple(self._num_blocks)}
        while True:
            largest_bank = self._largest_bank(num_blocks)
            num_blocks[largest_bank.index] = 0
            blocks_per_position = largest_bank.num_blocks // len(num_blocks)
            leftover_blocks = largest_bank.num_blocks % len(num_blocks)
            for i in range(len(num_blocks)):
                idx = (i + largest_bank.index + 1) % len(num_blocks)
                num_blocks[idx] += blocks_per_position
                if leftover_blocks > 0:
                    num_blocks[idx] += 1
                    leftover_blocks -= 1
            yield tuple(num_blocks)
            if tuple(num_blocks) in visited:
                break
            visited.add(tuple(num_blocks))
