from models.common.vectors import Vector3D


def _surface_area_of_single_cube(cube: Vector3D, other_cubes: set[Vector3D]) -> int:
    return sum(
        int(neighbor not in other_cubes)
        for neighbor in cube.adjacent_positions(include_diagonals=False)
    )


def total_surface_area(cubes: set[Vector3D]) -> int:
    return sum(_surface_area_of_single_cube(cube, cubes) for cube in cubes)
