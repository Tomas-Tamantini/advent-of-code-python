from models.aoc_2021 import Orientation
from models.vectors import Vector3D


def test_orientation_z_axis_is_vector_product_of_x_and_y_axis():
    orientation = Orientation(
        x_prime=Vector3D(0, 1, 0),
        y_prime=Vector3D(0, 0, -1),
    )
    assert orientation.z_prime == Vector3D(-1, 0, 0)


def test_there_are_24_orientations_aligned_with_grid_axes():
    orientations = Orientation.all_orientations_aligned_with_grid_axes()
    assert len(list(orientations)) == 24


def test_coordinates_in_given_orientation_can_be_reverted_to_absolute_coordinates():
    orientation = Orientation(
        x_prime=Vector3D(0, 1, 0),
        y_prime=Vector3D(0, 0, -1),
    )
    absolute_coordinates = orientation.to_absolute_coordinates(Vector3D(1, 2, 3))
    assert absolute_coordinates == Vector3D(-3, 1, -2)
