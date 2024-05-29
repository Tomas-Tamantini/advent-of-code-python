from dataclasses import dataclass
from math import ceil, inf
from typing import Iterator
from itertools import combinations


@dataclass(frozen=True)
class RpgItem:
    name: str
    cost: int
    damage: int
    armor: int


@dataclass(frozen=True)
class Fighter:
    hit_points: int
    damage: int
    armor: int

    def damage_per_round(self, other: "Fighter") -> int:
        return max(1, self.damage - other.armor)

    def hits_to_beat(self, other: "Fighter") -> int:
        return ceil(other.hit_points / self.damage_per_round(other))

    def beats_if_goes_first(self, other: "Fighter") -> bool:
        return self.hits_to_beat(other) <= other.hits_to_beat(self)

    @classmethod
    def from_items(cls, hit_points: int, *items: RpgItem) -> "Fighter":
        return cls(
            hit_points,
            damage=sum(item.damage for item in items),
            armor=sum(item.armor for item in items),
        )


class ItemAssortment:
    def __init__(
        self, items: list[RpgItem], min_num_items: int, max_num_items: int
    ) -> None:
        self._items = items
        self._min_num_items = min_num_items
        self._max_num_items = max_num_items

    def combinations(self) -> Iterator[set[RpgItem]]:
        for num_items in range(self._min_num_items, self._max_num_items + 1):
            yield from combinations(self._items, num_items)


class ItemShop:
    def __init__(
        self,
        weapons: ItemAssortment,
        armors: ItemAssortment,
        rings: ItemAssortment,
    ) -> None:
        self._weapons = weapons
        self._armors = armors
        self._rings = rings

    def cheapest_winning_items(
        self, my_hit_points: int, opponent: Fighter
    ) -> tuple[RpgItem]:
        min_cost = inf
        winning_items = None
        for weapon in self._weapons.combinations():
            for armor in self._armors.combinations():
                for rings in self._rings.combinations():
                    items = weapon + armor + rings
                    cost = sum(item.cost for item in items)
                    if cost > min_cost:
                        continue
                    player = Fighter.from_items(my_hit_points, *items)
                    if player.beats_if_goes_first(opponent):
                        min_cost = cost
                        winning_items = items

        return winning_items

    def most_expensive_losing_items(
        self, my_hit_points: int, opponent: Fighter
    ) -> tuple[RpgItem]:
        max_cost = -inf
        losing_items = None
        for weapon in self._weapons.combinations():
            for armor in self._armors.combinations():
                for rings in self._rings.combinations():
                    items = weapon + armor + rings
                    cost = sum(item.cost for item in items)
                    if cost < max_cost:
                        continue
                    player = Fighter.from_items(my_hit_points, *items)
                    if not player.beats_if_goes_first(opponent):
                        max_cost = cost
                        losing_items = items

        return losing_items
