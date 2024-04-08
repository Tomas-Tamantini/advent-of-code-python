from models.vectors import Vector2D
from models.aoc_2019 import BeamArea, run_beam_scanner, square_closest_to_beam_source


def test_beam_area_iterates_through_its_xy_coordinates():
    area = BeamArea(width=3, height=2)
    coordinates = list(area.coordinates())
    assert len(coordinates) == 6
    assert set(coordinates) == {
        Vector2D(0, 0),
        Vector2D(1, 0),
        Vector2D(2, 0),
        Vector2D(0, 1),
        Vector2D(1, 1),
        Vector2D(2, 1),
    }


def test_no_points_are_attracted_to_beam_by_default():
    area = BeamArea(width=3, height=3)
    assert area.num_points_attracted_to_beam == 0


def test_can_indicate_which_points_are_attracted_to_beam():
    area = BeamArea(width=3, height=3)
    area.set_point_attracted_to_beam(Vector2D(1, 1))
    area.set_point_attracted_to_beam(Vector2D(2, 2))
    assert area.num_points_attracted_to_beam == 2


def test_beam_scanner_runs_program_for_each_coordinate_in_beam_area():
    area = BeamArea(width=3, height=4)
    # Attraction only in x=1 coordinates:
    instructions = [3, 11, 3, 13, 8, 11, 12, 11, 4, 11, 99, -1, 1]
    run_beam_scanner(instructions, beam_area=area)
    assert area.num_points_attracted_to_beam == 4


def test_beam_scanner_finds_closest_square_which_fully_fits_inside_beam():
    scanned_area = BeamArea(width=10, height=10)
    # Attraction only in y<x<2y coordinates:
    instructions = [
        3,
        1_001,  # Input x
        3,
        1_002,  # Input y,
        102,
        2,
        1_002,
        1_003,  # Store 2*y
        7,
        1_002,
        1_001,
        1_004,  # y < x
        7,
        1_001,
        1_003,
        1_005,  # x < 2y
        1,
        1_004,
        1_005,
        1_006,  # y<x<2y
        108,
        2,
        1_006,
        1_007,  # 1 if y<x<2y else 0
        4,
        1_007,  # Output
        99,
    ]
    run_beam_scanner(instructions, beam_area=scanned_area)
    side_length = 4
    square_position = square_closest_to_beam_source(
        side_length, instructions, scanned_area
    )
    assert square_position.x == 12
    assert square_position.y == 8
