import pytest

from models.common.vectors import Vector3D

from ..logic import external_surface_area, total_surface_area


@pytest.mark.parametrize("area_func", [total_surface_area, external_surface_area])
def test_surface_area_of_zero_cubes_is_zero(area_func):
    cubes = set()
    assert area_func(cubes) == 0


@pytest.mark.parametrize("area_func", [total_surface_area, external_surface_area])
def test_surface_area_of_single_cube_is_six(area_func):
    cubes = {Vector3D(0, 0, 0)}
    assert area_func(cubes) == 6


@pytest.mark.parametrize("area_func", [total_surface_area, external_surface_area])
def test_surface_area_of_two_adjacent_cubes_is_ten(area_func):
    cubes = {Vector3D(0, 0, 0), Vector3D(1, 0, 0)}
    assert area_func(cubes) == 10


def test_total_surface_area_includes_internal_air_pockets():
    cubes = {Vector3D(x, y, z) for x in range(3) for y in range(3) for z in range(3)}
    cubes.remove(Vector3D(1, 1, 1))
    assert total_surface_area(cubes) == 60


def test_external_surface_area_excludes_internal_air_pockets():
    cubes = {Vector3D(x, y, z) for x in range(3) for y in range(3) for z in range(3)}
    cubes.remove(Vector3D(1, 1, 1))
    assert external_surface_area(cubes) == 54
