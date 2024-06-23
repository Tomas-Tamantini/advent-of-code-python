from models.common.io import IOHandler
from .parser import parse_rpg_boss
from .rpg_game import Fighter, ItemAssortment, RpgItem, ItemShop


def aoc_2015_d21(io_handler: IOHandler) -> None:
    print("--- AOC 2015 - Day 21: RPG Simulator 20XX ---")
    my_hit_points = 100
    boss_kwargs = parse_rpg_boss(io_handler.input_reader)
    boss = Fighter(**boss_kwargs)
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

    winning_items = shop.cheapest_winning_items(my_hit_points, opponent=boss)
    min_cost = sum(item.cost for item in winning_items)
    print(f"Part 1: Cheapest winning items cost {min_cost}")
    losing_items = shop.most_expensive_losing_items(my_hit_points, opponent=boss)
    max_cost = sum(item.cost for item in losing_items)
    print(f"Part 2: Most expensive losing items cost {max_cost}")
