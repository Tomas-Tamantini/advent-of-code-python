import pytest
from models.vectors import Vector3D
from models.aoc_2021 import Cuboid


def test_can_iterate_through_all_points_inside_cuboid():
    cuboid = Cuboid(
        range_start=Vector3D(1, 2, 3),
        range_end=Vector3D(3, 3, 4),
    )
    cells_within = list(cuboid.cells_within())
    assert len(cells_within) == 12
    assert set(cells_within) == {
        Vector3D(1, 2, 3),
        Vector3D(1, 2, 4),
        Vector3D(1, 3, 3),
        Vector3D(1, 3, 4),
        Vector3D(2, 2, 3),
        Vector3D(2, 2, 4),
        Vector3D(2, 3, 3),
        Vector3D(2, 3, 4),
        Vector3D(3, 2, 3),
        Vector3D(3, 2, 4),
        Vector3D(3, 3, 3),
        Vector3D(3, 3, 4),
    }


@pytest.mark.parametrize(
    "min_x, max_x, min_y, max_y, min_z, maz_z, expected",
    [
        (1, 10, -10, 10, 0, 1, True),
        (0, 0, 1, 1, 2, 2, True),
        (5, 11, 0, 0, 0, 0, False),
        (5, 10, -11, 0, 0, 0, False),
        (0, 0, 0, 0, -3, 11, False),
    ],
)
def test_cuboid_checks_if_all_its_coordinates_are_within_given_range(
    min_x, max_x, min_y, max_y, min_z, maz_z, expected
):
    cuboid = Cuboid(
        range_start=Vector3D(min_x, min_y, min_z),
        range_end=Vector3D(max_x, max_y, maz_z),
    )
    assert expected == cuboid.all_coords_between(-10, 10)
