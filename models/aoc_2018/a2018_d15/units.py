from dataclasses import dataclass
from typing import Iterator
from models.vectors import Vector2D, CardinalDirection


@dataclass(frozen=True)
class CaveGameUnit:
    unit_id: str
    hit_points: int
    attack_power: int
    position: Vector2D

    def _updated_position(self, direction: CardinalDirection) -> Vector2D:
        mirrored_direction = (
            direction if direction.is_horizontal else direction.reverse()
        )
        return self.position.move(mirrored_direction)

    @property
    def is_dead(self) -> bool:
        return self.hit_points <= 0

    def move(self, direction: CardinalDirection) -> "CaveGameUnit":
        return CaveGameUnit(
            unit_id=self.unit_id,
            hit_points=self.hit_points,
            attack_power=self.attack_power,
            position=self._updated_position(direction),
        )

    def take_damage(self, damage: int) -> "CaveGameUnit":
        new_hp = max(0, self.hit_points - damage)
        return CaveGameUnit(
            unit_id=self.unit_id,
            hit_points=new_hp,
            attack_power=self.attack_power,
            position=self.position,
        )

    def adjacent_positions_in_reading_order(self) -> Iterator[Vector2D]:
        for direction in CardinalDirection.reading_order():
            yield self._updated_position(direction)
