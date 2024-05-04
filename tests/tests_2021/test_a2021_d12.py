from models.aoc_2021 import UnderwaterCave, UnderwaterCaveExplorer


def test_underwater_cave_explorer_cannot_go_from_start_to_end_if_no_path():
    explorer = UnderwaterCaveExplorer(connections=dict())
    assert list(explorer.all_paths(start_cave_name="start", end_cave_name="end")) == []


def test_underwater_cave_explorer_can_go_from_start_to_end_if_at_least_one_path():
    start = UnderwaterCave(name="start", is_small=True)
    end = UnderwaterCave(name="end", is_small=True)
    middle = UnderwaterCave(name="middle", is_small=True)
    explorer = UnderwaterCaveExplorer(connections={start: {middle}, middle: {end}})
    assert list(explorer.all_paths(start_cave_name="start", end_cave_name="end")) == [
        [start, middle, end]
    ]


def test_underwater_cave_explorer_yields_all_paths_from_start_to_end():
    start = UnderwaterCave(name="start", is_small=True)
    end = UnderwaterCave(name="end", is_small=True)
    middle_a = UnderwaterCave(name="middle_a", is_small=True)
    middle_b = UnderwaterCave(name="middle_b", is_small=True)
    explorer = UnderwaterCaveExplorer(
        connections={start: {middle_a, middle_b}, end: {middle_a, middle_b}}
    )
    assert list(explorer.all_paths(start_cave_name="start", end_cave_name="end")) == [
        [start, middle_a, end],
        [start, middle_b, end],
    ]


def test_large_caves_can_be_visited_more_than_once():
    start = UnderwaterCave(name="start", is_small=True)
    end = UnderwaterCave(name="end", is_small=True)
    large_a = UnderwaterCave(name="large_a", is_small=False)
    small_b = UnderwaterCave(name="small_b", is_small=True)
    small_c = UnderwaterCave(name="small_c", is_small=True)
    small_d = UnderwaterCave(name="small_d", is_small=True)
    explorer = UnderwaterCaveExplorer(
        connections={
            start: {large_a, small_b},
            large_a: {small_b, small_c, end},
            small_b: {end, small_d},
        }
    )
    paths = list(explorer.all_paths(start_cave_name="start", end_cave_name="end"))
    assert len(paths) == 10
