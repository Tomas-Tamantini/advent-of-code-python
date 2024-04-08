from models.aoc_2019 import BeamArea, run_beam_scanner


def test_beam_area_iterates_through_its_xy_coordinates():
    area = BeamArea(width=3, height=2)
    coordinates = list(area.coordinates())
    assert len(coordinates) == 6
    assert set(coordinates) == {(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1)}


def test_no_points_are_attracted_to_beam_by_default():
    area = BeamArea(width=3, height=3)
    assert area.num_points_attracted_to_beam == 0


def test_can_indicate_which_points_are_attracted_to_beam():
    area = BeamArea(width=3, height=3)
    area.set_point_attracted_to_beam(x=1, y=1)
    area.set_point_attracted_to_beam(x=2, y=2)
    assert area.num_points_attracted_to_beam == 2


def test_beam_scanner_runs_program_for_each_coordinate_in_beam_area():
    area = BeamArea(width=3, height=4)
    # Attraction only in x=1 coordinates:
    instructions = [3, 11, 3, 13, 8, 11, 12, 11, 4, 11, 99, -1, 1]
    run_beam_scanner(instructions, beam_area=area)
    assert area.num_points_attracted_to_beam == 4
