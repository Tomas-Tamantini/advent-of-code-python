import pytest
from models.vectors import Vector2D, TurnDirection, CardinalDirection
from models.aoc_2019.a2019_d17 import (
    ScaffoldMap,
    CameraOutput,
    run_scaffolding_program,
    VacuumRobotInstruction,
    compress_vacuum_bot_path,
)


def test_scaffold_map_starts_empty():
    sm = ScaffoldMap()
    assert sm.render() == ""


def test_can_add_pixels_to_scaffold_map():
    sm = ScaffoldMap()
    sm.add_pixel("#")
    sm.add_pixel(".")
    sm.add_pixel("v")
    sm.add_pixel("\n")
    sm.add_pixel("#")
    sm.add_pixel("#")
    sm.add_pixel("#")

    assert sm.render() == "#.v\n###"


def _build_scaffold(map_str: str) -> ScaffoldMap:
    sm = ScaffoldMap()
    for line in map_str.split("\n"):
        for pixel in line.strip():
            sm.add_pixel(pixel)
        sm.add_pixel("\n")
    return sm


def test_can_iterate_through_scaffolding_intersections():
    sm = _build_scaffold("#.#.\n####\n#.#.\n")
    assert list(sm.scaffolding_intersections()) == [Vector2D(0, 1), Vector2D(2, 1)]


def test_can_find_position_and_direction_of_vacuum_bot():
    sm = _build_scaffold("...\n..^")
    assert sm.vacuum_robot.position == Vector2D(2, 1)
    assert sm.vacuum_robot.direction == CardinalDirection.NORTH


_example_path = [
    VacuumRobotInstruction(TurnDirection.RIGHT, 8),
    VacuumRobotInstruction(TurnDirection.RIGHT, 8),
    VacuumRobotInstruction(TurnDirection.RIGHT, 4),
    VacuumRobotInstruction(TurnDirection.RIGHT, 4),
    VacuumRobotInstruction(TurnDirection.RIGHT, 8),
    VacuumRobotInstruction(TurnDirection.LEFT, 6),
    VacuumRobotInstruction(TurnDirection.LEFT, 2),
    VacuumRobotInstruction(TurnDirection.RIGHT, 4),
    VacuumRobotInstruction(TurnDirection.RIGHT, 4),
    VacuumRobotInstruction(TurnDirection.RIGHT, 8),
    VacuumRobotInstruction(TurnDirection.RIGHT, 8),
    VacuumRobotInstruction(TurnDirection.RIGHT, 8),
    VacuumRobotInstruction(TurnDirection.LEFT, 6),
    VacuumRobotInstruction(TurnDirection.LEFT, 2),
]


def test_can_find_path_through_scaffolding():
    map_str = """#######...#####
                 #.....#...#...#
                 #.....#...#...#
                 ......#...#...#
                 ......#...###.#
                 ......#.....#.#
                 ^########...#.#
                 ......#.#...#.#
                 ......#########
                 ........#...#..
                 ....#########..
                 ....#...#......
                 ....#...#......
                 ....#...#......
                 ....#####......"""
    sm = _build_scaffold(map_str)
    assert list(sm.path_through_scaffolding()) == _example_path


@pytest.mark.skip("Not implemented")
def test_path_through_scaffolding_can_be_compressed():
    expected_main_routine = "A,B,C,B,A,C"
    expected_subroutines = {
        "A": "R,8,R,8",
        "B": "R,4,R,4,R,8",
        "C": "L,6,L,2",
    }
    compressed = compress_vacuum_bot_path(_example_path, num_subroutines=3)
    assert compressed.main_routine == expected_main_routine
    assert compressed.subroutines == expected_subroutines


def test_camera_output_converts_value_to_ascii_and_builds_map():
    sm = ScaffoldMap()
    co = CameraOutput(sm)
    co.write(35)
    co.write(46)
    co.write(118)
    co.write(10)
    co.write(35)
    co.write(35)
    co.write(35)

    assert sm.render() == "#.v\n###"


def test_can_run_scaffolding_program_to_build_map():
    instructions = [104, 35, 99]
    sm = ScaffoldMap()
    run_scaffolding_program(sm, instructions)
    assert sm.render() == "#"
