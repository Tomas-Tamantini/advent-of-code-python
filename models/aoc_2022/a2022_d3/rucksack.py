from dataclasses import dataclass
from typing import Iterator


@dataclass(frozen=True)
class Rucksack:
    left_items: str
    right_items: str

    def items_in_common_between_left_and_right(self) -> Iterator[chr]:
        yield from set(self.left_items) & set(self.right_items)

    def _all_items(self) -> set[chr]:
        return set(self.left_items) | set(self.right_items)

    def items_in_common_with_others(self, *other: "Rucksack") -> Iterator[chr]:
        all_items = self._all_items()
        for rucksack in other:
            all_items &= rucksack._all_items()
        yield from all_items

    @staticmethod
    def item_priority(item: chr) -> int:
        if item.islower():
            return ord(item) - ord("a") + 1
        else:
            return ord(item) - ord("A") + 27
