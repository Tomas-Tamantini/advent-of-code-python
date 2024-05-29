from ..rpg_game import Fighter, ItemAssortment, RpgItem, ItemShop

boss = Fighter(hit_points=12, damage=7, armor=2)


def test_damage_dealt_per_round_is_damage_minus_armor():
    player = Fighter(hit_points=8, damage=5, armor=5)
    assert player.damage_per_round(boss) == 3
    assert boss.damage_per_round(player) == 2


def test_damage_dealt_per_round_is_at_least_one():
    player = Fighter(hit_points=8, damage=0, armor=5)
    assert player.damage_per_round(boss) == 1


def test_can_calculate_number_of_hits_to_beat_opponent():
    player = Fighter(hit_points=8, damage=5, armor=5)
    assert player.hits_to_beat(boss) == 4
    assert boss.hits_to_beat(player) == 4


def test_first_fighter_to_reach_zero_hit_points_loses():
    player = Fighter(hit_points=8, damage=5, armor=5)
    assert player.beats_if_goes_first(boss) == True


def test_items_determine_damage_and_armor():
    items = [
        RpgItem(name="Dagger", cost=8, damage=4, armor=2),
        RpgItem(name="Leather", cost=13, damage=0, armor=1),
    ]
    hit_points = 8
    player = Fighter.from_items(hit_points, *items)
    assert player.hit_points == 8
    assert player.damage == 4
    assert player.armor == 3


def test_can_loop_through_all_possible_item_assortments():
    assortment = ItemAssortment(
        items=["a", "b", "c"],
        min_num_items=0,
        max_num_items=2,
    )
    assert list(assortment.combinations()) == [
        (),
        ("a",),
        ("b",),
        ("c",),
        ("a", "b"),
        ("a", "c"),
        ("b", "c"),
    ]


weapons = ItemAssortment(
    items=[
        RpgItem(name="Dagger", cost=8, damage=4, armor=0),
        RpgItem(name="Shortsword", cost=10, damage=5, armor=0),
        RpgItem(name="Warhammer", cost=25, damage=6, armor=0),
        RpgItem(name="Longsword", cost=40, damage=7, armor=0),
        RpgItem(name="Greataxe", cost=74, damage=8, armor=0),
    ],
    min_num_items=1,
    max_num_items=1,
)

armors = ItemAssortment(
    items=[
        RpgItem(name="Leather", cost=13, damage=0, armor=1),
        RpgItem(name="Chainmail", cost=31, damage=0, armor=2),
        RpgItem(name="Splintmail", cost=53, damage=0, armor=3),
        RpgItem(name="Bandedmail", cost=75, damage=0, armor=4),
        RpgItem(name="Platemail", cost=102, damage=0, armor=5),
    ],
    min_num_items=0,
    max_num_items=1,
)

rings = ItemAssortment(
    items=[
        RpgItem(name="Damage +1", cost=25, damage=1, armor=0),
        RpgItem(name="Damage +2", cost=50, damage=2, armor=0),
        RpgItem(name="Damage +3", cost=100, damage=3, armor=0),
        RpgItem(name="Defense +1", cost=20, damage=0, armor=1),
        RpgItem(name="Defense +2", cost=40, damage=0, armor=2),
        RpgItem(name="Defense +3", cost=80, damage=0, armor=3),
    ],
    min_num_items=0,
    max_num_items=2,
)

shop = ItemShop(weapons, armors, rings)


def test_can_pick_cheapest_items_to_beat_opponent():
    my_hit_points = 8
    expected_items = {"Longsword", "Damage +1"}
    winning_items = shop.cheapest_winning_items(my_hit_points, opponent=boss)
    assert {item.name for item in winning_items} == expected_items


def test_can_pick_most_expensive_items_that_still_loses_to_opponent():
    my_hit_points = 8
    expected_items = {"Dagger", "Defense +3", "Damage +3"}
    winning_items = shop.most_expensive_losing_items(my_hit_points, opponent=boss)
    assert {item.name for item in winning_items} == expected_items
