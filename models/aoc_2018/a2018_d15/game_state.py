from dataclasses import dataclass
from typing import Iterator
from models.vectors import Vector2D
from .units import CaveGameUnit


@dataclass(frozen=True)
class CaveGameState:
    elves: tuple[CaveGameUnit]
    goblins: tuple[CaveGameUnit]

    @property
    def total_hp(self) -> int:
        return sum(unit.hit_points for unit in self.elves + self.goblins)

    def has_duplicate_ids(self) -> bool:
        unit_ids = {unit.unit_id for unit in self.elves + self.goblins}
        return len(unit_ids) != len(self.elves) + len(self.goblins)

    def get_unit_from_id(self, unit_id: str) -> CaveGameUnit:
        for unit in self.elves + self.goblins:
            if unit.unit_id == unit_id:
                return unit
        raise ValueError(f"Unknown unit id: {unit_id}")

    def _opponent_team(self, unit: CaveGameUnit) -> tuple[CaveGameUnit]:
        elf_ids = {elf.unit_id for elf in self.elves}
        return self.goblins if unit.unit_id in elf_ids else self.elves

    def game_is_over(self) -> bool:
        return len(self.elves) == 0 or len(self.goblins) == 0

    def target_positions(self, unit) -> Iterator[Vector2D]:
        for opponent in self._opponent_team(unit):
            yield from opponent.adjacent_positions_in_reading_order()

    def adjacent_opponents(self, unit: CaveGameUnit) -> Iterator[CaveGameUnit]:
        opponent_positions = {
            opponent.position: opponent for opponent in self._opponent_team(unit)
        }
        for position in unit.adjacent_positions_in_reading_order():
            if position in opponent_positions:
                yield opponent_positions[position]

    def units_in_reading_order(self) -> Iterator[CaveGameUnit]:
        all_units = self.elves + self.goblins
        yield from sorted(all_units, key=lambda c: (c.position.y, c.position.x))
