from dataclasses import dataclass
from typing import Optional, Iterable
from .army_group import ArmyGroup


@dataclass(frozen=True)
class InfectionGameState:
    infection_armies: tuple[ArmyGroup, ...]
    immune_system_armies: tuple[ArmyGroup, ...]

    @property
    def total_num_units(self) -> int:
        return sum(
            group.num_units
            for group in self.infection_armies + self.immune_system_armies
        )

    @property
    def is_over(self) -> bool:
        return not self.infection_armies or not self.immune_system_armies

    def boost_immune_system_attack_power(self, boost: int) -> "InfectionGameState":
        return InfectionGameState(
            infection_armies=self.infection_armies,
            immune_system_armies=tuple(
                group.boost_attack_power(boost) for group in self.immune_system_armies
            ),
        )

    @staticmethod
    def _choose_targets(
        attacking_groups: tuple[ArmyGroup, ...],
        defending_groups: tuple[ArmyGroup, ...],
    ) -> dict[ArmyGroup, ArmyGroup]:
        targets = {}
        for attacking_group in sorted(
            attacking_groups,
            key=lambda group: (-group.effective_power, -group.initiative),
        ):
            valid_targets = [
                group
                for group in defending_groups
                if group not in targets.values()
                and attacking_group.damage_that_can_be_dealt_to(group) > 0
            ]
            target = InfectionGameState._choose_target(attacking_group, valid_targets)
            if target is not None:
                targets[attacking_group] = target
        return targets

    @staticmethod
    def _choose_target(
        attacking_group: ArmyGroup, valid_targets: Iterable[ArmyGroup]
    ) -> Optional[ArmyGroup]:
        target = max(
            (group for group in valid_targets),
            key=lambda group: (
                attacking_group.damage_that_can_be_dealt_to(group),
                group.effective_power,
                group.initiative,
            ),
            default=None,
        )
        return target

    def targets(self) -> dict[ArmyGroup, ArmyGroup]:
        infection_targets = self._choose_targets(
            attacking_groups=self.infection_armies,
            defending_groups=self.immune_system_armies,
        )
        immune_system_targets = self._choose_targets(
            attacking_groups=self.immune_system_armies,
            defending_groups=self.infection_armies,
        )
        return {**infection_targets, **immune_system_targets}

    def play_round(self) -> "InfectionGameState":
        targets = self.targets()
        all_groups = sorted(
            self.infection_armies + self.immune_system_armies,
            key=lambda group: -group.initiative,
        )

        new_groups = {
            group.group_id: group
            for group in self.infection_armies + self.immune_system_armies
        }

        for group in all_groups:
            updated_group = new_groups.get(group.group_id)
            if updated_group is None:
                continue
            target = targets.get(group)
            if target is None:
                continue
            damage = updated_group.damage_that_can_be_dealt_to(target)
            new_target = target.take_damage(damage)
            if new_target.is_dead:
                del new_groups[target.group_id]
            else:
                new_groups[target.group_id] = new_target

        new_infection_armies = tuple(
            new_groups[group.group_id]
            for group in self.infection_armies
            if group.group_id in new_groups
        )

        new_immune_system_armies = tuple(
            new_groups[group.group_id]
            for group in self.immune_system_armies
            if group.group_id in new_groups
        )

        state_after = InfectionGameState(
            infection_armies=new_infection_armies,
            immune_system_armies=new_immune_system_armies,
        )
        if self.total_num_units == state_after.total_num_units:
            raise ValueError("Tie: No change in total number of units")

        return state_after
