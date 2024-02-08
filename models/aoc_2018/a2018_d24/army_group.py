from dataclasses import dataclass
from typing import Hashable
from .attack_types import AttackType


@dataclass(frozen=True)
class ArmyGroup:
    group_id: Hashable
    num_units: int
    hit_points_per_unit: int
    attack_damage_per_unit: int
    initiative: int
    attack_type: AttackType
    weaknesses: tuple[AttackType]
    immunities: tuple[AttackType]

    @property
    def is_dead(self):
        return self.num_units <= 0

    @property
    def effective_power(self):
        return self.num_units * self.attack_damage_per_unit

    def damage_that_can_be_dealt_to(self, other: "ArmyGroup") -> int:
        if self.attack_type in other.immunities:
            return 0
        elif self.attack_type in other.weaknesses:
            return self.effective_power * 2
        else:
            return self.effective_power

    def take_damage(self, damage: int) -> "ArmyGroup":
        num_units_killed = damage // self.hit_points_per_unit
        return ArmyGroup(
            group_id=self.group_id,
            num_units=max(0, self.num_units - num_units_killed),
            hit_points_per_unit=self.hit_points_per_unit,
            attack_damage_per_unit=self.attack_damage_per_unit,
            initiative=self.initiative,
            attack_type=self.attack_type,
            weaknesses=self.weaknesses,
            immunities=self.immunities,
        )

    def boost_attack_power(self, boost: int) -> "ArmyGroup":
        return ArmyGroup(
            group_id=self.group_id,
            num_units=self.num_units,
            hit_points_per_unit=self.hit_points_per_unit,
            attack_damage_per_unit=self.attack_damage_per_unit + boost,
            initiative=self.initiative,
            attack_type=self.attack_type,
            weaknesses=self.weaknesses,
            immunities=self.immunities,
        )
