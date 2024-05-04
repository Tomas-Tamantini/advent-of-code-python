from models.aoc_2021 import UnderwaterCave, UnderwaterCaveExplorer


def test_underwater_cave_explorer_cannot_go_from_start_to_end_if_no_path():
    explorer = UnderwaterCaveExplorer(
        connections=dict(), start_cave_name="start", end_cave_name="end"
    )
    assert list(explorer.all_paths()) == []


def test_underwater_cave_explorer_can_go_from_start_to_end_if_at_least_one_path():
    start = UnderwaterCave(name="start", is_small=True)
    end = UnderwaterCave(name="end", is_small=True)
    middle = UnderwaterCave(name="middle", is_small=True)
    explorer = UnderwaterCaveExplorer(
        connections={start: {middle}, middle: {end}},
        start_cave_name="start",
        end_cave_name="end",
    )
    assert list(explorer.all_paths()) == [[start, middle, end]]


def test_underwater_cave_explorer_yields_all_paths_from_start_to_end():
    start = UnderwaterCave(name="start", is_small=True)
    end = UnderwaterCave(name="end", is_small=True)
    middle_a = UnderwaterCave(name="middle_a", is_small=True)
    middle_b = UnderwaterCave(name="middle_b", is_small=True)
    explorer = UnderwaterCaveExplorer(
        connections={start: {middle_a, middle_b}, end: {middle_a, middle_b}},
        start_cave_name="start",
        end_cave_name="end",
    )
    paths = list(explorer.all_paths())
    assert len(paths) == 2
    paths_set = {tuple(path) for path in paths}
    assert paths_set == {(start, middle_a, end), (start, middle_b, end)}


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
        },
        start_cave_name="start",
        end_cave_name="end",
    )
    paths = list(explorer.all_paths())
    assert len(paths) == 10


def test_one_small_caves_may_be_visited_twice_if_specified():
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
        },
        start_cave_name="start",
        end_cave_name="end",
    )
    paths = list(explorer.all_paths(may_visit_one_small_cave_twice=True))
    assert len(paths) == 36
