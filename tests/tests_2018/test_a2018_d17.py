from models.vectors import Vector2D
from models.aoc_2018 import WaterSpring


def test_spring_can_be_converted_to_string():
    spring = WaterSpring(
        spring_position=Vector2D(0, 0),
        clay_positions={
            Vector2D(1_000, 1_000),
            Vector2D(1_001, 1_000),
            Vector2D(1_002, 1_002),
        },
    )
    assert str(spring) == "\n".join(
        [
            "##.",
            "...",
            "..#",
        ]
    )


def test_spring_starts_with_no_wet_tiles():
    spring = WaterSpring(spring_position=Vector2D(0, 0), clay_positions=set())
    assert spring.num_wet_tiles == 0


def test_water_flows_down_if_no_obstacles():
    spring = WaterSpring(
        spring_position=Vector2D(1, -1000),
        clay_positions={
            Vector2D(0, 0),
            Vector2D(3, 2),
        },
    )
    spring.flow()
    assert spring.num_wet_tiles == 3
    assert str(spring) == "\n".join(
        [
            "#|..",
            ".|..",
            ".|.#",
        ]
    )


def _str_to_spring(spring_layout: list[str]) -> WaterSpring:
    clay_positions = set()
    spring_position = Vector2D(0, 0)
    for y, row in enumerate(spring_layout):
        for x, tile in enumerate(row):
            if tile == "#":
                clay_positions.add(Vector2D(x, y))
            elif tile == "+":
                spring_position = Vector2D(x, y)
    return WaterSpring(spring_position, clay_positions)


def test_water_flows_sideways_if_blocked_from_below():
    spring = _str_to_spring(
        [
            "#...+....",
            ".........",
            "...####..",
            ".........",
            ".........",
            "..#......",
            "........#",
        ]
    )
    expected = "\n".join(
        [
            "#...|....",
            "..||||||.",
            "..|####|.",
            "..|....|.",
            ".|||...|.",
            ".|#|...|.",
            ".|.|...|#",
        ]
    )
    spring.flow()
    assert str(spring) == expected
    assert spring.num_wet_tiles == 21


def test_water_can_be_contained_by_clay_wall():
    spring = _str_to_spring(
        [
            "#...+.....",
            "..#.......",
            "..#####...",
            "........#.",
            "........#.",
            "....#####.",
            ".........#",
        ]
    )
    expected = "\n".join(
        [
            "#...|.....",
            "..#|||||..",
            "..#####|..",
            ".......|#.",
            "...|||||#.",
            "...|#####.",
            "...|.....#",
        ]
    )
    spring.flow()
    assert str(spring) == expected
    assert spring.num_wet_tiles == 15


def test_water_contained_on_both_sides_becomes_still():
    spring = _str_to_spring(
        [
            "#.#.+.....",
            "..#...#...",
            "..#.......",
            "..#....#..",
            "..#....#..",
            "..######..",
            "..........",
            ".........#",
            "...#.....#",
            "...#######",
            "..........",
            "..##......",
        ]
    )
    expected = "\n".join(
        [
            "#.#.|.....",
            "..#.|.#...",
            "..#||||||.",
            "..#~~~~#|.",
            "..#~~~~#|.",
            "..######|.",
            "........|.",
            "..|||||||#",
            "..|#~~~~~#",
            "..|#######",
            ".||||.....",
            ".|##|.....",
        ]
    )
    spring.flow()
    assert str(spring) == expected
    assert spring.num_wet_tiles == 40


def test_there_is_no_water_pressure_to_keep_it_level_on_both_sides_of_container():
    spring = _str_to_spring(
        [
            "......+.....#.",
            ".#..#.......#.",
            ".#..#..#......",
            ".#..#..#......",
            ".#.....#......",
            ".#.....#......",
            ".#######......",
            "..............",
            "..............",
            "....#.....#...",
            "....#.....#...",
            "....#.....#...",
            "#...#######..#",
        ]
    )
    expected = "\n".join(
        [
            "......|.....#.",
            ".#..#||||...#.",
            ".#..#~~#|.....",
            ".#..#~~#|.....",
            ".#~~~~~#|.....",
            ".#~~~~~#|.....",
            ".#######|.....",
            "........|.....",
            "...|||||||||..",
            "...|#~~~~~#|..",
            "...|#~~~~~#|..",
            "...|#~~~~~#|..",
            "#..|#######|.#",
        ]
    )
    spring.flow()
    assert str(spring) == expected
    assert spring.num_wet_tiles == 57
