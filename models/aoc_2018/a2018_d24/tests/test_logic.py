from random import choice

import pytest

from ..logic import (
    ArmyGroup,
    AttackType,
    InfectionGame,
    InfectionGameState,
    optimal_boost_for_immune_system,
)


def _build_army_group(**kwargs) -> ArmyGroup:
    defaults = {
        "group_id": "".join(choice("abcdefghijklmnopqrstuvwxyz") for _ in range(20)),
        "num_units": 1,
        "hit_points_per_unit": 1,
        "attack_damage_per_unit": 1,
        "initiative": 1,
        "attack_type": AttackType.SLASHING,
        "weaknesses": tuple(),
        "immunities": tuple(),
    }
    defaults.update(kwargs)
    return ArmyGroup(**defaults)


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


def test_armies_choose_targets_from_enemy_groups():
    group_immune_system = _build_army_group()
    group_infection = _build_army_group()
    game_state = InfectionGameState(
        infection_armies=(group_infection,), immune_system_armies=(group_immune_system,)
    )
    targets = game_state.targets()
    assert targets == {
        group_immune_system: group_infection,
        group_infection: group_immune_system,
    }


def test_groups_choose_targets_in_decreasing_order_of_effective_power():
    group_immune_system_a = _build_army_group(num_units=10, attack_damage_per_unit=3)
    group_immune_system_b = _build_army_group(num_units=20, attack_damage_per_unit=3)
    group_infection = _build_army_group(num_units=10, attack_damage_per_unit=3)
    game_state = InfectionGameState(
        infection_armies=(group_infection,),
        immune_system_armies=(group_immune_system_a, group_immune_system_b),
    )
    targets = game_state.targets()
    assert group_immune_system_a not in targets
    assert targets[group_immune_system_b] == group_infection


def test_groups_which_tie_effective_power_choose_targets_by_initiative():
    group_immune_system_a = _build_army_group(
        num_units=10, attack_damage_per_unit=3, initiative=2
    )
    group_immune_system_b = _build_army_group(
        num_units=10, attack_damage_per_unit=3, initiative=3
    )
    group_infection = _build_army_group(num_units=10, attack_damage_per_unit=3)
    game_state = InfectionGameState(
        infection_armies=(group_infection,),
        immune_system_armies=(group_immune_system_a, group_immune_system_b),
    )
    targets = game_state.targets()
    assert group_immune_system_a not in targets
    assert targets[group_immune_system_b] == group_infection


def test_group_chooses_target_which_it_can_deal_most_damage_to():
    group_immune_system = _build_army_group(attack_type=AttackType.SLASHING)
    group_infection_a = _build_army_group()
    group_infection_b = _build_army_group(weaknesses=(AttackType.SLASHING,))
    game_state = InfectionGameState(
        infection_armies=(group_infection_a, group_infection_b),
        immune_system_armies=(group_immune_system,),
    )
    targets = game_state.targets()
    assert targets[group_immune_system] == group_infection_b


def test_if_damage_ties_choose_target_by_larger_effective_power():
    group_immune_system = _build_army_group(attack_damage_per_unit=3)
    group_infection_a = _build_army_group(num_units=10, attack_damage_per_unit=3)
    group_infection_b = _build_army_group(num_units=20, attack_damage_per_unit=3)
    game_state = InfectionGameState(
        infection_armies=(group_infection_a, group_infection_b),
        immune_system_armies=(group_immune_system,),
    )
    targets = game_state.targets()
    assert targets[group_immune_system] == group_infection_b


def test_if_damage_and_effective_power_tie_choose_target_by_larger_initiative():
    group_immune_system = _build_army_group(attack_damage_per_unit=3, initiative=2)
    group_infection_a = _build_army_group(
        num_units=10, attack_damage_per_unit=3, initiative=2
    )
    group_infection_b = _build_army_group(
        num_units=10, attack_damage_per_unit=3, initiative=3
    )
    game_state = InfectionGameState(
        infection_armies=(group_infection_a, group_infection_b),
        immune_system_armies=(group_immune_system,),
    )
    targets = game_state.targets()
    assert targets[group_immune_system] == group_infection_b


def test_if_group_cannot_deal_damage_to_any_enemies_it_chooses_no_target():
    group_immune_system = _build_army_group(attack_type=AttackType.SLASHING)
    group_infection = _build_army_group(immunities=(AttackType.SLASHING,))
    game_state = InfectionGameState(
        infection_armies=(group_infection,),
        immune_system_armies=(group_immune_system,),
    )
    targets = game_state.targets()
    assert group_immune_system not in targets
    assert targets[group_infection] == group_immune_system


def test_playing_round_raises_exception_if_no_possible_moves():
    group_immune_system = _build_army_group(
        attack_type=AttackType.SLASHING,
        immunities=(AttackType.FIRE,),
    )
    group_infection = _build_army_group(
        attack_type=AttackType.FIRE,
        immunities=(AttackType.SLASHING,),
    )
    game_state = InfectionGameState(
        infection_armies=(group_infection,),
        immune_system_armies=(group_immune_system,),
    )
    with pytest.raises(ValueError):
        _ = game_state.play_round()


sample_game = InfectionGameState(
    immune_system_armies=(
        _build_army_group(
            group_id="Immune 1",
            num_units=17,
            hit_points_per_unit=5390,
            attack_damage_per_unit=4507,
            attack_type=AttackType.FIRE,
            initiative=2,
            weaknesses=(AttackType.RADIATION, AttackType.BLUDGEONING),
        ),
        _build_army_group(
            group_id="Immune 2",
            num_units=989,
            hit_points_per_unit=1274,
            attack_damage_per_unit=25,
            attack_type=AttackType.SLASHING,
            initiative=3,
            immunities=(AttackType.FIRE,),
            weaknesses=(AttackType.BLUDGEONING, AttackType.SLASHING),
        ),
    ),
    infection_armies=(
        _build_army_group(
            group_id="Infection 1",
            num_units=801,
            hit_points_per_unit=4706,
            attack_damage_per_unit=116,
            attack_type=AttackType.BLUDGEONING,
            initiative=1,
            weaknesses=(AttackType.RADIATION,),
        ),
        _build_army_group(
            group_id="Infection 2",
            num_units=4485,
            hit_points_per_unit=2961,
            attack_damage_per_unit=12,
            attack_type=AttackType.SLASHING,
            initiative=4,
            weaknesses=(AttackType.FIRE,),
            immunities=(AttackType.RADIATION,),
        ),
    ),
)


def test_each_group_deals_damage_to_its_target_during_round():
    updated_state = sample_game.play_round()
    assert updated_state.infection_armies[0].num_units == 797
    assert updated_state.infection_armies[1].num_units == 4434


def test_groups_are_removed_from_game_if_all_units_died():
    updated_state = sample_game.play_round()
    assert len(updated_state.immune_system_armies) == 1
    assert updated_state.immune_system_armies[0].num_units == 905


def test_can_get_total_num_units():
    assert sample_game.total_num_units == 6292


def test_game_is_not_over_if_both_sides_have_units():
    assert not sample_game.is_over


def test_game_is_over_if_one_side_has_no_units():
    game = InfectionGameState(
        immune_system_armies=[_build_army_group(num_units=1)],
        infection_armies=[],
    )
    assert game.is_over


def test_can_run_infection_game_until_completion():
    game = InfectionGame(sample_game)
    game.run_until_over()
    assert game.state.is_over
    assert game.state.total_num_units == 5216


def test_can_boost_attack_power_of_all_immune_system_armies():
    new_state = sample_game.boost_immune_system_attack_power(1570)
    assert new_state.immune_system_armies[0].attack_damage_per_unit == 6077
    assert new_state.immune_system_armies[1].attack_damage_per_unit == 1595


def test_can_determine_whether_immune_system_won_game():
    game_loss = InfectionGame(sample_game)
    game_loss.run_until_over()
    assert not game_loss.immune_system_won

    game_win = InfectionGame(sample_game.boost_immune_system_attack_power(1570))
    game_win.run_until_over()
    assert game_win.immune_system_won


def test_can_find_optimal_boost_to_immune_system_to_ensure_its_victory():
    boost, game_state = optimal_boost_for_immune_system(sample_game)
    assert boost == 1570
    assert game_state.total_num_units == 51
