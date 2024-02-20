from models.vectors import Vector3D
from models.aoc_2019 import MoonOfJupiter, MoonSystem


def test_two_moons_with_same_given_coordinate_do_not_attract_each_other():
    moon_a = MoonOfJupiter(position=Vector3D(x=123), velocity=Vector3D(x=100))
    moon_b = MoonOfJupiter(position=Vector3D(x=123), velocity=Vector3D(x=-300))
    moon_a.apply_gravity(moon_b)
    assert moon_a.velocity.x == 100
    assert moon_b.velocity.x == -300


def test_two_moons_with_different_given_coordinates_update_velocity_in_each_other_direction_by_one():
    moon_a = MoonOfJupiter(position=Vector3D(y=1234), velocity=Vector3D(y=100))
    moon_b = MoonOfJupiter(position=Vector3D(y=123), velocity=Vector3D(y=-300))
    moon_a.apply_gravity(moon_b)
    assert moon_a.velocity.y == 99
    assert moon_b.velocity.y == -299


def test_moon_of_jupiter_can_apply_velocity_to_its_position():
    moon = MoonOfJupiter(
        position=Vector3D(x=1, y=2, z=3), velocity=Vector3D(x=10, y=20, z=30)
    )
    moon.apply_velocity()
    assert moon.position == Vector3D(x=11, y=22, z=33)
    assert moon.velocity == Vector3D(x=10, y=20, z=30)


def test_moon_system_updates_all_moons_simultaneously():
    system = MoonSystem(
        moons=[
            MoonOfJupiter(position=Vector3D(-1, 0, 2)),
            MoonOfJupiter(position=Vector3D(2, -10, -7)),
            MoonOfJupiter(position=Vector3D(4, -8, 8)),
            MoonOfJupiter(position=Vector3D(3, 5, -1)),
        ]
    )
    system.step()
    assert system.moons[0].position == Vector3D(2, -1, 1)
    assert system.moons[1].position == Vector3D(3, -7, -4)
    assert system.moons[2].position == Vector3D(1, -7, 5)
    assert system.moons[3].position == Vector3D(2, 2, 0)


def test_system_can_take_multiple_steps_at_once():
    system = MoonSystem(
        moons=[
            MoonOfJupiter(Vector3D(-8, -10, 0)),
            MoonOfJupiter(Vector3D(5, 5, 10)),
            MoonOfJupiter(Vector3D(2, -7, 3)),
            MoonOfJupiter(Vector3D(9, -8, -3)),
        ]
    )
    system.multi_step(num_steps=100)
    assert system.moons[0].position == Vector3D(8, -12, -9)
    assert system.moons[1].position == Vector3D(13, 16, -3)
    assert system.moons[2].position == Vector3D(-29, -11, -1)
    assert system.moons[3].position == Vector3D(16, -13, 23)
