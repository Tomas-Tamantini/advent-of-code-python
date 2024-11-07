from models.common.vectors import Vector3D
from ..logic import Hailstone, rock_that_hits_all_hailstones


def _hailstones_example(x_offset: int = 0) -> list[Hailstone]:
    return [
        Hailstone(
            position=Vector3D(x_offset + 19, 13, 30), velocity=Vector3D(-2, 1, -2)
        ),
        Hailstone(
            position=Vector3D(x_offset + 18, 19, 22), velocity=Vector3D(-1, -1, -2)
        ),
        Hailstone(
            position=Vector3D(x_offset + 20, 25, 34), velocity=Vector3D(-2, -2, -4)
        ),
        Hailstone(
            position=Vector3D(x_offset + 12, 31, 28), velocity=Vector3D(-1, -2, -1)
        ),
        Hailstone(
            position=Vector3D(x_offset + 20, 19, 15), velocity=Vector3D(1, -5, -3)
        ),
    ]


def test_rock_that_hits_all_hailstones_has_position_and_velocity_calculated():
    hailstones = _hailstones_example()
    rock = rock_that_hits_all_hailstones(hailstones)
    assert rock == Hailstone(position=Vector3D(24, 13, 10), velocity=Vector3D(-3, 1, 2))


def test_rock_that_hits_all_hailstones_is_calculated_exactly():
    x_offset = 1_000_000_000_000_000_000
    hailstones = _hailstones_example(x_offset)
    rock = rock_that_hits_all_hailstones(hailstones)
    assert rock == Hailstone(
        position=Vector3D(x_offset + 24, 13, 10),
        velocity=Vector3D(-3, 1, 2),
    )
