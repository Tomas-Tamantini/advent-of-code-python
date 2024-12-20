import pytest

from models.common.vectors import Vector3D

from ..reactor_cells import Cuboid, CuboidInstruction, num_reactor_cells_on


def _build_cuboid(
    x_range: tuple[int, int], y_range: tuple[int, int], z_range: tuple[int, int]
) -> Cuboid:
    return Cuboid(
        range_start=Vector3D(x_range[0], y_range[0], z_range[0]),
        range_end=Vector3D(x_range[1], y_range[1], z_range[1]),
    )


def test_cuboid_volume_is_number_of_cells_within_it():
    cuboid = _build_cuboid((1, 3), (2, 3), (3, 4))
    assert cuboid.volume() == 12


def test_intersection_of_two_non_overlapping_cuboids_is_none():
    cuboid_1 = _build_cuboid((1, 3), (2, 3), (3, 4))
    cuboid_2 = _build_cuboid((4, 6), (5, 5), (6, 8))
    assert cuboid_1.intersect(cuboid_2) is None


def test_intersection_of_overlapping_cuboids_is_cuboid():
    cuboid_1 = _build_cuboid((1, 3), (2, 3), (3, 4))
    cuboid_2 = _build_cuboid((2, 4), (3, 4), (4, 9))
    intersection = cuboid_1.intersect(cuboid_2)
    assert intersection == _build_cuboid((2, 3), (3, 3), (4, 4))


@pytest.mark.parametrize(
    ("x_range", "y_range", "z_range", "expected"),
    [
        ((1, 10), (-10, 10), (0, 1), True),
        ((0, 0), (1, 1), (2, 2), True),
        ((5, 11), (0, 0), (0, 0), False),
        ((5, 10), (-11, 0), (0, 0), False),
        ((0, 0), (0, 0), (-3, 11), False),
    ],
)
def test_cuboid_checks_if_all_its_coordinates_are_within_given_range(
    x_range, y_range, z_range, expected
):
    cuboid = _build_cuboid(x_range, y_range, z_range)
    assert expected == cuboid.all_coords_are_between(-10, 10)


def test_number_of_reactor_cells_on_with_zero_instructions_is_zero():
    assert num_reactor_cells_on(instructions=[]) == 0


def test_number_of_reactor_cells_with_single_on_instruction_is_cuboid_volume():
    instruction = CuboidInstruction(
        cuboid=_build_cuboid((1, 3), (2, 3), (3, 4)),
        is_turn_on=True,
    )
    assert num_reactor_cells_on(instructions=[instruction]) == 12


def test_number_of_reactor_cells_with_multiple_non_overlapping_on_instructions_is_sum_of_cuboid_volumes():
    instructions = [
        CuboidInstruction(
            cuboid=_build_cuboid((1, 3), (2, 3), (3, 4)), is_turn_on=True
        ),
        CuboidInstruction(
            cuboid=_build_cuboid((4, 6), (5, 5), (6, 8)), is_turn_on=True
        ),
    ]
    assert num_reactor_cells_on(instructions=instructions) == 21


def test_number_of_reactor_cells_with_some_off_instruction_removes_cells_from_off_instruction():
    instructions = [
        CuboidInstruction(
            cuboid=_build_cuboid((1, 10), (1, 10), (1, 10)), is_turn_on=True
        ),
        CuboidInstruction(
            cuboid=_build_cuboid((8, 99), (8, 99), (8, 99)), is_turn_on=False
        ),
    ]
    assert num_reactor_cells_on(instructions=instructions) == 973


def test_number_of_reactor_cells_with_overlapping_on_instructions_is_sum_of_cuboid_volumes_minus_intersections_calculated_recursively():
    instructions = [
        CuboidInstruction(
            cuboid=_build_cuboid((10, 12), (10, 12), (10, 12)), is_turn_on=True
        ),
        CuboidInstruction(
            cuboid=_build_cuboid((11, 13), (11, 13), (11, 13)), is_turn_on=True
        ),
        CuboidInstruction(
            cuboid=_build_cuboid((9, 11), (9, 11), (9, 11)), is_turn_on=False
        ),
        CuboidInstruction(
            cuboid=_build_cuboid((10, 10), (10, 10), (10, 10)), is_turn_on=True
        ),
    ]
    assert num_reactor_cells_on(instructions=instructions) == 39
