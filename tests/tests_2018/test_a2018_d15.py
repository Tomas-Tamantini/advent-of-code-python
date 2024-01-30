import pytest
from models.vectors import Vector2D, CardinalDirection
from models.aoc_2018.a2018_d15 import (
    CaveTile,
    CaveMap,
    CaveGameUnit,
    CaveGameState,
    MoveUnit,
    AttackMove,
    CaveGameBotAttackWeakest,
    CaveGame,
    CaveTeamSpec,
    build_cave_game,
    optimal_game_for_elves,
)

map_string = "\n".join(
    [
        "#######",
        "#......",
        "#......",
    ]
)


def test_can_build_map_from_string():
    cave_map = CaveMap(map_string)
    for x in range(7):
        assert cave_map.get_tile(x, 0) == CaveTile.WALL
    for y in range(1, 3):
        assert cave_map.get_tile(0, y) == CaveTile.WALL
        for x in range(1, 7):
            assert cave_map.get_tile(x, y) == CaveTile.OPEN


def test_trying_to_get_out_of_bound_tiles_returns_wall():
    cave_map = CaveMap(map_string)
    assert cave_map.get_tile(-1, 0) == CaveTile.WALL
    assert cave_map.get_tile(7, 0) == CaveTile.WALL
    assert cave_map.get_tile(0, -1) == CaveTile.WALL
    assert cave_map.get_tile(0, 3) == CaveTile.WALL


def _build_game_unit(
    unit_id: str = "C",
    hit_points: int = 200,
    attack_power: int = 3,
    position: Vector2D = Vector2D(0, 0),
) -> CaveGameUnit:
    return CaveGameUnit(
        unit_id=unit_id,
        hit_points=hit_points,
        attack_power=attack_power,
        position=position,
    )


def test_can_set_unit_attack_power():
    unit = _build_game_unit(attack_power=3)
    new_unit = unit.set_attack_power(5)
    assert new_unit.attack_power == 5


def test_unit_can_take_damage():
    unit = _build_game_unit(hit_points=200)
    new_unit = unit.take_damage(3)
    assert new_unit.hit_points == 197


def test_unit_can_move_in_four_directions():
    unit = _build_game_unit(position=Vector2D(1, 1))
    new_unit = unit.move(CardinalDirection.NORTH)
    assert new_unit.position == Vector2D(1, 0)
    new_unit = unit.move(CardinalDirection.EAST)
    assert new_unit.position == Vector2D(2, 1)
    new_unit = unit.move(CardinalDirection.SOUTH)
    assert new_unit.position == Vector2D(1, 2)
    new_unit = unit.move(CardinalDirection.WEST)
    assert new_unit.position == Vector2D(0, 1)


def test_unit_is_dead_if_hp_drops_to_zero_or_below():
    assert _build_game_unit(hit_points=0).is_dead == True
    assert _build_game_unit(hit_points=-1).is_dead == True
    assert _build_game_unit(hit_points=1).is_dead == False


def test_unit_can_iterate_through_adjacent_positions_in_reading_order():
    unit = _build_game_unit(position=Vector2D(1, 1))
    assert list(unit.adjacent_positions_in_reading_order()) == [
        Vector2D(1, 0),
        Vector2D(0, 1),
        Vector2D(2, 1),
        Vector2D(1, 2),
    ]


def test_game_is_over_if_some_team_lost_all_players():
    game_state = CaveGameState(
        elves=tuple(),
        goblins=(_build_game_unit(),),
    )
    assert game_state.game_is_over() == True

    game_state = CaveGameState(
        elves=(_build_game_unit(),),
        goblins=set(),
    )
    assert game_state.game_is_over() == True


def test_game_is_not_over_if_both_teams_have_players():
    game_state = CaveGameState(
        elves=(_build_game_unit("Elf"),),
        goblins=(_build_game_unit("Goblin"),),
    )
    assert game_state.game_is_over() == False


def test_target_positions_are_ones_adjacent_to_opponents():
    elf = _build_game_unit(position=Vector2D(1, 1), unit_id="Elf")
    goblin_a = _build_game_unit(position=Vector2D(10, 10), unit_id="gA")
    goblin_b = _build_game_unit(position=Vector2D(11, 11), unit_id="gB")
    game_state = CaveGameState(
        elves=(elf,),
        goblins=(goblin_a, goblin_b),
    )
    assert set(game_state.target_positions(elf)) == {
        Vector2D(9, 10),
        Vector2D(10, 9),
        Vector2D(10, 11),
        Vector2D(11, 10),
        Vector2D(12, 11),
        Vector2D(11, 12),
    }
    assert set(game_state.target_positions(goblin_a)) == {
        Vector2D(0, 1),
        Vector2D(1, 0),
        Vector2D(2, 1),
        Vector2D(1, 2),
    }


def test_can_iterate_through_units_in_reading_order():
    elf_a = _build_game_unit(position=Vector2D(10, 1))
    elf_b = _build_game_unit(position=Vector2D(2, 2))
    goblin_a = _build_game_unit(position=Vector2D(1, 1))
    goblin_b = _build_game_unit(position=Vector2D(3, 2))
    game_state = CaveGameState(
        elves=(elf_a, elf_b),
        goblins=(goblin_a, goblin_b),
    )
    assert list(game_state.units_in_reading_order()) == [
        goblin_a,
        elf_a,
        elf_b,
        goblin_b,
    ]


def test_can_iterate_through_adjacent_opponents_in_reading_order():
    elf = _build_game_unit(position=Vector2D(1, 1), unit_id="Elf")
    goblin_up = _build_game_unit(position=Vector2D(1, 0), unit_id="Goblin Up")
    goblin_down = _build_game_unit(position=Vector2D(1, 2), unit_id="Goblin Down")
    goblin_left = _build_game_unit(position=Vector2D(0, 1), unit_id="Goblin Left")
    goblin_right = _build_game_unit(position=Vector2D(2, 1), unit_id="Goblin Right")
    goblin_diagonal = _build_game_unit(
        position=Vector2D(2, 2), unit_id="Goblin Diagonal"
    )

    game_state = CaveGameState(
        elves=(elf,),
        goblins=(goblin_right, goblin_left, goblin_down, goblin_up, goblin_diagonal),
    )
    assert list(game_state.adjacent_opponents(elf)) == [
        goblin_up,
        goblin_left,
        goblin_right,
        goblin_down,
    ]
    assert list(game_state.adjacent_opponents(goblin_up)) == [elf]


def test_can_get_unit_from_id():
    elf_a = _build_game_unit(position=Vector2D(10, 1), unit_id="Elf A")
    elf_b = _build_game_unit(position=Vector2D(2, 2), unit_id="Elf B")
    game_state = CaveGameState(
        elves=(elf_a, elf_b),
        goblins=tuple(),
    )
    assert game_state.get_unit_from_id("Elf A") == elf_a
    assert game_state.get_unit_from_id("Elf B") == elf_b


def test_can_set_whole_team_attack_power():
    game_state = CaveGameState(
        elves=(
            _build_game_unit(unit_id="Elf A", attack_power=3),
            _build_game_unit(unit_id="Elf B", attack_power=2),
        ),
        goblins=tuple(),
    )
    new_game_state = game_state.set_elf_attack_power(5)
    assert new_game_state.elves == (
        _build_game_unit(unit_id="Elf A", attack_power=5),
        _build_game_unit(unit_id="Elf B", attack_power=5),
    )


def test_can_move_unit_from_some_team():
    elf = _build_game_unit(position=Vector2D(1, 1), unit_id="Elf")
    goblin = _build_game_unit(position=Vector2D(10, 10), unit_id="Goblin")
    game_state = CaveGameState(elves=(elf,), goblins=(goblin,))
    move_up = MoveUnit(direction=CardinalDirection.NORTH)
    new_game_state = move_up.execute(elf, game_state)
    assert new_game_state.elves == (
        _build_game_unit(position=Vector2D(1, 0), unit_id="Elf"),
    )
    assert new_game_state.goblins == (goblin,)


def test_units_can_attack_one_another():
    elf = _build_game_unit(unit_id="Elf", attack_power=3)
    goblin = _build_game_unit(unit_id="Goblin", hit_points=200)

    game_state = CaveGameState(elves=(elf,), goblins=(goblin,))
    attack = AttackMove(target=goblin)
    new_game_state = attack.execute(elf, game_state)
    assert new_game_state.elves == (elf,)
    assert new_game_state.goblins == (
        _build_game_unit(unit_id="Goblin", hit_points=197),
    )


def test_unit_who_dies_is_removed_from_game():
    elf = _build_game_unit(unit_id="Elf", attack_power=3)
    goblin = _build_game_unit(unit_id="Goblin", hit_points=3)

    game_state = CaveGameState(elves=(elf,), goblins=(goblin,))
    attack = AttackMove(target=goblin)
    new_game_state = attack.execute(elf, game_state)
    assert new_game_state.elves == (elf,)
    assert new_game_state.goblins == tuple()


def test_bot_returns_no_move_if_unit_is_walled_in():
    cave_map = CaveMap(
        "\n".join(
            [
                "######",
                "#..#.#",
                "######",
            ]
        )
    )
    elf = _build_game_unit(position=Vector2D(1, 1), unit_id="Elf")
    goblin = _build_game_unit(position=Vector2D(4, 1), unit_id="Goblin")
    game_state = CaveGameState(elves=(elf,), goblins=(goblin,))
    moves = CaveGameBotAttackWeakest().bot_moves(
        unit=elf, game_state=game_state, cave_map=cave_map
    )
    assert len(list(moves)) == 0


def test_bot_returns_no_move_if_unit_is_walled_in_by_allies():
    cave_map = CaveMap(
        "\n".join(
            [
                "#####",
                "#...#",
                "#####",
            ]
        )
    )
    elf_a = _build_game_unit(position=Vector2D(1, 1), unit_id="Elf A")
    elf_b = _build_game_unit(position=Vector2D(2, 1), unit_id="Elf B")
    goblin = _build_game_unit(position=Vector2D(3, 1), unit_id="Goblin")
    game_state = CaveGameState(elves=(elf_a, elf_b), goblins=(goblin,))
    moves = CaveGameBotAttackWeakest().bot_moves(
        unit=elf_a, game_state=game_state, cave_map=cave_map
    )
    assert len(list(moves)) == 0


def test_if_opponents_are_in_range_bot_attacks_weakest_one_with_tie_decided_by_reading_order():
    cave_map = CaveMap(
        "\n".join(
            [
                "...",
                "#.#",
            ]
        )
    )
    elf = _build_game_unit(position=Vector2D(1, 0), unit_id="Elf")
    goblin_left = _build_game_unit(
        position=Vector2D(0, 0), unit_id="Goblin A", hit_points=3
    )
    goblin_right = _build_game_unit(
        position=Vector2D(2, 0), unit_id="Goblin B", hit_points=2
    )
    goblin_down = _build_game_unit(
        position=Vector2D(2, 1), unit_id="Goblin C", hit_points=2
    )

    game_state = CaveGameState(
        elves=(elf,), goblins=(goblin_down, goblin_left, goblin_right)
    )
    moves = list(
        CaveGameBotAttackWeakest().bot_moves(
            unit=elf, game_state=game_state, cave_map=cave_map
        )
    )
    assert len(moves) == 1
    assert isinstance(moves[0], AttackMove)
    assert moves[0].target == goblin_right


def test_if_no_opponent_in_range_unit_moves_in_direction_of_closest_range_with_tie_broken_by_reading_order():
    cave_map = CaveMap(
        "\n".join(
            [
                "...",
                "#..",
                "...",
            ]
        )
    )
    elf = _build_game_unit(position=Vector2D(1, 0))
    goblin_left = _build_game_unit(position=Vector2D(0, 2), unit_id="Goblin A")
    goblin_right = _build_game_unit(position=Vector2D(2, 2), unit_id="Goblin B")

    game_state = CaveGameState(elves=(elf,), goblins=(goblin_left, goblin_right))

    moves_elf = list(
        CaveGameBotAttackWeakest().bot_moves(
            unit=elf, game_state=game_state, cave_map=cave_map
        )
    )
    assert len(moves_elf) == 1
    assert isinstance(moves_elf[0], MoveUnit)
    assert moves_elf[0].direction == CardinalDirection.EAST

    moves_goblin_left = list(
        CaveGameBotAttackWeakest().bot_moves(
            unit=goblin_left, game_state=game_state, cave_map=cave_map
        )
    )
    assert len(moves_goblin_left) == 1
    assert isinstance(moves_goblin_left[0], MoveUnit)
    assert moves_goblin_left[0].direction == CardinalDirection.EAST

    moves_goblin_right = list(
        CaveGameBotAttackWeakest().bot_moves(
            unit=goblin_right, game_state=game_state, cave_map=cave_map
        )
    )
    assert len(moves_goblin_right) == 1
    assert isinstance(moves_goblin_right[0], MoveUnit)
    assert moves_goblin_right[0].direction == CardinalDirection.NORTH


def test_unit_attacks_in_same_turn_if_movement_brought_it_in_range():
    cave_map = CaveMap("...")
    elf = _build_game_unit(position=Vector2D(0, 0), unit_id="Elf")
    goblin = _build_game_unit(position=Vector2D(2, 0), unit_id="Goblin")
    game_state = CaveGameState(elves=(elf,), goblins=(goblin,))

    moves_elf = list(
        CaveGameBotAttackWeakest().bot_moves(
            unit=elf, game_state=game_state, cave_map=cave_map
        )
    )
    assert len(moves_elf) == 2
    assert isinstance(moves_elf[0], MoveUnit)
    assert moves_elf[0].direction == CardinalDirection.EAST
    assert isinstance(moves_elf[1], AttackMove)
    assert moves_elf[1].target == goblin

    moves_goblin = list(
        CaveGameBotAttackWeakest().bot_moves(
            unit=goblin, game_state=game_state, cave_map=cave_map
        )
    )
    assert len(moves_goblin) == 2
    assert isinstance(moves_goblin[0], MoveUnit)
    assert moves_goblin[0].direction == CardinalDirection.WEST
    assert isinstance(moves_goblin[1], AttackMove)
    assert moves_goblin[1].target == elf


def test_game_must_contain_unique_ids():
    bad_state = CaveGameState(
        elves=(_build_game_unit(unit_id="Elf"), _build_game_unit(unit_id="Elf")),
        goblins=tuple(),
    )
    with pytest.raises(ValueError):
        _ = CaveGame(cave_map=CaveMap("."), initial_units=bad_state)


def test_game_starts_at_round_zero():
    game = CaveGame(
        cave_map=CaveMap("."),
        initial_units=CaveGameState(
            elves=(_build_game_unit(unit_id="E"),),
            goblins=(_build_game_unit(unit_id="G"),),
        ),
    )
    assert game.round == 0


example_maps = [
    [
        "#######",
        "#.G...#",
        "#...EG#",
        "#.#.#G#",
        "#..G#E#",
        "#.....#",
        "#######",
    ],
    [
        "#######",
        "#G..#E#",
        "#E#E.E#",
        "#G.##.#",
        "#...#E#",
        "#...E.#",
        "#######",
    ],
    [
        "#######",
        "#E..EG#",
        "#.#G.E#",
        "#E.##E#",
        "#G..#.#",
        "#..E#.#",
        "#######",
    ],
    [
        "#######",
        "#E.G#.#",
        "#.#G..#",
        "#G.#.G#",
        "#G..#.#",
        "#...E.#",
        "#######",
    ],
    [
        "#######",
        "#.E...#",
        "#.#..G#",
        "#.###.#",
        "#E#G#G#",
        "#...#G#",
        "#######",
    ],
    [
        "#########",
        "#G......#",
        "#.E.#...#",
        "#..##..G#",
        "#...##..#",
        "#...#...#",
        "#.G...G.#",
        "#.....G.#",
        "#########",
    ],
]


def test_can_build_game_from_string():
    elf_team_spec = CaveTeamSpec(attack_power=2, hit_points=200)
    goblin_team_spec = CaveTeamSpec(attack_power=3, hit_points=100)
    map_str = "\n".join(example_maps[0])
    game = build_cave_game(
        map_with_units=map_str, elf_specs=elf_team_spec, goblin_specs=goblin_team_spec
    )
    assert game.state.elves == (
        _build_game_unit(
            unit_id="E1", position=Vector2D(4, 2), attack_power=2, hit_points=200
        ),
        _build_game_unit(
            unit_id="E2", position=Vector2D(5, 4), attack_power=2, hit_points=200
        ),
    )
    assert game.state.goblins == (
        _build_game_unit(
            unit_id="G1", position=Vector2D(2, 1), attack_power=3, hit_points=100
        ),
        _build_game_unit(
            unit_id="G2", position=Vector2D(5, 2), attack_power=3, hit_points=100
        ),
        _build_game_unit(
            unit_id="G3", position=Vector2D(5, 3), attack_power=3, hit_points=100
        ),
        _build_game_unit(
            unit_id="G4", position=Vector2D(3, 4), attack_power=3, hit_points=100
        ),
    )
    assert game._map.get_tile(0, 0) == CaveTile.WALL
    assert game._map.get_tile(1, 1) == CaveTile.OPEN
    assert game._map.get_tile(2, 1) == CaveTile.OPEN


def test_game_from_str_assumes_hp_200_and_attack_power_3_by_default():
    map_str = "EG"
    game = build_cave_game(map_with_units=map_str)
    assert game.state.elves == (
        _build_game_unit(unit_id="E1", position=Vector2D(0, 0)),
    )
    assert game.state.goblins == (
        _build_game_unit(unit_id="G1", position=Vector2D(1, 0)),
    )


def test_game_can_be_played_by_bots_until_it_is_over():
    game = build_cave_game("\n".join(example_maps[0]))
    game.play_until_over(bot=CaveGameBotAttackWeakest())
    assert game.round == 47
    assert game.state.game_is_over()
    assert game.state.elves == tuple()
    assert game.state.goblins == (
        _build_game_unit(unit_id="G1", position=Vector2D(1, 1), hit_points=200),
        _build_game_unit(unit_id="G2", position=Vector2D(2, 2), hit_points=131),
        _build_game_unit(unit_id="G3", position=Vector2D(5, 3), hit_points=59),
        _build_game_unit(unit_id="G4", position=Vector2D(5, 5), hit_points=200),
    )


@pytest.mark.parametrize(
    "map_as_list, expected_num_rounds, expected_hp",
    [
        (example_maps[1], 37, 982),
        (example_maps[2], 46, 859),
        (example_maps[3], 35, 793),
        (example_maps[4], 54, 536),
        (example_maps[5], 20, 937),
    ],
)
def test_can_query_total_hp_after_cave_game_is_over(
    map_as_list, expected_num_rounds, expected_hp
):
    game = build_cave_game("\n".join(map_as_list))
    game.play_until_over(bot=CaveGameBotAttackWeakest())
    assert game.round == expected_num_rounds
    assert game.state.total_hp == expected_hp


def test_can_calculate_number_of_casualties_throughout_game():
    game = build_cave_game("\n".join(example_maps[2]))
    assert game.elf_casualties == game.goblin_casualties == 0
    game.play_until_over(bot=CaveGameBotAttackWeakest())
    assert game.elf_casualties == 1
    assert game.goblin_casualties == 3


@pytest.mark.parametrize(
    "map_as_list, expected_num_rounds, expected_hp, expected_attack_power",
    [
        (example_maps[0], 29, 172, 15),
        (example_maps[2], 33, 948, 4),
        (example_maps[3], 37, 94, 15),
        (example_maps[4], 39, 166, 12),
        (example_maps[5], 30, 38, 34),
    ],
)
def test_can_find_smallest_attack_power_that_ensures_elf_victory_without_casualties(
    map_as_list, expected_num_rounds, expected_hp, expected_attack_power
):
    game = build_cave_game("\n".join(map_as_list))
    result = optimal_game_for_elves(game, bot=CaveGameBotAttackWeakest())
    assert result.rounds == expected_num_rounds
    assert result.hp_remaining == expected_hp
    assert result.elf_attack_power == expected_attack_power
