from models.common.vectors import Vector3D
from ..logic import total_surface_area


def test_surface_area_of_zero_cubes_is_zero():
    cubes = set()
    assert total_surface_area(cubes) == 0


def test_surface_area_of_single_cube_is_six():
    cubes = {Vector3D(0, 0, 0)}
    assert total_surface_area(cubes) == 6


def test_surface_area_of_two_adjacent_cubes_is_ten():
    cubes = {Vector3D(0, 0, 0), Vector3D(1, 0, 0)}
    assert total_surface_area(cubes) == 10


def test_total_surface_area_includes_internal_air_pockets():
    cubes = {Vector3D(x, y, z) for x in range(3) for y in range(3) for z in range(3)}
    cubes.remove(Vector3D(1, 1, 1))
    assert total_surface_area(cubes) == 60
