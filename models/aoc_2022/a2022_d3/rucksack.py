from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Rucksack:
    left_items: str
    right_items: str

    def items_in_common(self) -> Iterator[chr]:
        yield from set(self.left_items) & set(self.right_items)

    @staticmethod
    def item_priority(item: chr) -> int:
        if item.islower():
            return ord(item) - ord("a") + 1
        else:
            return ord(item) - ord("A") + 27
