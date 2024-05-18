import pytest
from models.common.vectors import Vector2D, TurnDirection, CardinalDirection
from models.aoc_2019.a2019_d17 import (
    ScaffoldMap,
    CameraOutput,
    VacuumRobotOutput,
    VacuumRobotInput,
    CompressedPath,
    run_scaffolding_discovery_program,
    run_scaffolding_exploration_program,
    VacuumRobotInstruction,
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


example_map = _build_scaffold(
    """#######...#####
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
)


def test_can_find_path_through_scaffolding():
    assert list(example_map.path_through_scaffolding()) == [
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


def test_path_through_scaffolding_can_be_compressed():
    expected_main_routine = "A,B,C,B,A,C"
    expected_subroutines = {
        "A": "R,8,R,8",
        "B": "R,4,R,4",
        "C": "R,8,L,6,L,2",
    }
    compressed = example_map.compressed_path_through_scaffolding(num_subroutines=3)
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


def test_running_scaffolding_discovery_program_builds_map():
    instructions = [104, 35, 99]
    sm = ScaffoldMap()
    run_scaffolding_discovery_program(sm, instructions)
    assert sm.render() == "#"


def test_vacuum_robot_output_stores_the_last_value():
    ro = VacuumRobotOutput()
    ro.write(35)
    assert ro.output_value == 35
    ro.write(46)
    ro.write(118)
    assert ro.output_value == 118


def test_vacuum_robot_input_yelds_ascii_values_for_compressed_path_main_and_subroutines_separated_by_new_line():
    compressed_path = CompressedPath(
        main_routine="A,B,A,C",
        subroutines={"A": "R,8", "B": "7", "C": "L,1,R,2"},
    )
    expected_input_stream = "A,B,A,C\nR,8\n7\nL,1,R,2\n"
    expected_ascii_values = [ord(c) for c in expected_input_stream]
    vi = VacuumRobotInput(compressed_path=compressed_path)
    for expected_ascii_value in expected_ascii_values:
        assert vi.read() == expected_ascii_value


@pytest.mark.parametrize("watch_feed", [True, False])
def test_vacuum_robot_input_yelds_y_or_n_and_new_line_as_the_last_two_characters_of_input(
    watch_feed,
):
    compressed_path = CompressedPath(
        main_routine="A",
        subroutines={"A": "1"},
    )
    watch = "y" if watch_feed else "n"
    expected_input_stream = f"A\n1\n{watch}\n"
    vi = VacuumRobotInput(compressed_path=compressed_path, watch_video_feed=watch_feed)
    expected_ascii_values = [ord(c) for c in expected_input_stream]
    for expected_ascii_value in expected_ascii_values:
        assert vi.read() == expected_ascii_value


def test_running_scaffolding_exploration_program_reads_robot_input_and_yields_output():
    instructions = [3, 100, 3, 100, 3, 100, 3, 100, 3, 200, 3, 100, 4, 200, 99]
    compressed_path = CompressedPath("A", {"A": "1"})
    output = run_scaffolding_exploration_program(
        instructions, compressed_path, watch_video_feed=True
    )
    assert output == 121  # ACII value of 'y'
