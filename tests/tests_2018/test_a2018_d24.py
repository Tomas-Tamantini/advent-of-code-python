from models.aoc_2018.a2018_d24 import AttackType, ArmyGroup


def _build_army_group(
    num_units: int = 1,
    hit_points_per_unit: int = 1,
    attack_damage_per_unit: int = 1,
    initiative: int = 1,
    attack_type: AttackType = AttackType.SLASHING,
    weaknesses: tuple[AttackType] = tuple(),
    immunities: tuple[AttackType] = tuple(),
) -> ArmyGroup:
    return ArmyGroup(
        num_units=num_units,
        hit_points_per_unit=hit_points_per_unit,
        attack_damage_per_unit=attack_damage_per_unit,
        initiative=initiative,
        attack_type=attack_type,
        weaknesses=weaknesses,
        immunities=immunities,
    )


def test_army_group_is_not_dead_if_some_unit_is_alive():
    army_group = _build_army_group(num_units=1)
    assert not army_group.is_dead


def test_army_group_is_dead_if_no_unit_is_alive():
    army_group = _build_army_group(num_units=0)
    assert army_group.is_dead


def test_effective_power_is_num_units_times_attack_damage():
    army_group = _build_army_group(num_units=10, attack_damage_per_unit=3)
    assert army_group.effective_power == 30


def test_group_deals_damage_equal_to_its_effective_power():
    attacking_group = _build_army_group(num_units=10, attack_damage_per_unit=3)
    defending_group = _build_army_group(num_units=10, hit_points_per_unit=10)
    assert attacking_group.damage_that_can_be_dealt_to(defending_group) == 30


def test_defending_group_immune_to_attack_type_takes_no_damage():
    attacking_group = _build_army_group(
        num_units=10, attack_damage_per_unit=3, attack_type=AttackType.SLASHING
    )
    defending_group = _build_army_group(
        num_units=10, hit_points_per_unit=10, immunities=(AttackType.SLASHING,)
    )
    assert attacking_group.damage_that_can_be_dealt_to(defending_group) == 0


def test_defending_group_weak_to_attack_type_takes_double_damage():
    attacking_group = _build_army_group(
        num_units=10, attack_damage_per_unit=3, attack_type=AttackType.SLASHING
    )
    defending_group = _build_army_group(
        num_units=10, hit_points_per_unit=10, weaknesses=(AttackType.SLASHING,)
    )
    assert attacking_group.damage_that_can_be_dealt_to(defending_group) == 60


def test_damage_taken_kills_whole_number_of_units():
    defending_group = _build_army_group(num_units=10, hit_points_per_unit=10)
    updated_defending_group = defending_group.take_damage(damage=75)
    assert updated_defending_group.num_units == 3
