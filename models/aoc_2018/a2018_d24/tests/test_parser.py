from models.common.io import InputFromString

from ..logic import ArmyGroup, AttackType
from ..parser import parse_infection_game


def test_parse_infection_game():
    file_content = """Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4"""
    game_state = parse_infection_game(InputFromString(file_content))
    assert game_state.immune_system_armies == (
        ArmyGroup(
            group_id=1,
            num_units=17,
            hit_points_per_unit=5390,
            attack_damage_per_unit=4507,
            attack_type=AttackType.FIRE,
            initiative=2,
            weaknesses=(AttackType.RADIATION, AttackType.BLUDGEONING),
            immunities=tuple(),
        ),
        ArmyGroup(
            group_id=2,
            num_units=989,
            hit_points_per_unit=1274,
            attack_damage_per_unit=25,
            attack_type=AttackType.SLASHING,
            initiative=3,
            immunities=(AttackType.FIRE,),
            weaknesses=(AttackType.BLUDGEONING, AttackType.SLASHING),
        ),
    )
    assert game_state.infection_armies == (
        ArmyGroup(
            group_id=3,
            num_units=801,
            hit_points_per_unit=4706,
            attack_damage_per_unit=116,
            attack_type=AttackType.BLUDGEONING,
            initiative=1,
            weaknesses=(AttackType.RADIATION,),
            immunities=tuple(),
        ),
        ArmyGroup(
            group_id=4,
            num_units=4485,
            hit_points_per_unit=2961,
            attack_damage_per_unit=12,
            attack_type=AttackType.SLASHING,
            initiative=4,
            immunities=(AttackType.RADIATION,),
            weaknesses=(AttackType.FIRE, AttackType.COLD),
        ),
    )
