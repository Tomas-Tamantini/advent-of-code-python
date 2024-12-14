from models.common.vectors import Particle2D, Vector2D

from .guarded_bathroom import GuardedBathroom


def test_bathroom_guards_wrap_around_like_pacman():
    bathroom = GuardedBathroom(width=11, height=7)
    guard = Particle2D(position=Vector2D(2, 4), velocity=Vector2D(2, -3))
    assert Vector2D(2, 4) == bathroom.guard_position_after_time(guard, time=0)
    assert Vector2D(4, 1) == bathroom.guard_position_after_time(guard, time=1)
    assert Vector2D(6, 5) == bathroom.guard_position_after_time(guard, time=2)
    assert Vector2D(1, 3) == bathroom.guard_position_after_time(guard, time=5)


def test_guarded_bathroom_counts_number_of_guards_per_quadrant():
    bathroom = GuardedBathroom(width=11, height=7)
    initial_guards = [
        Particle2D(Vector2D(0, 4), Vector2D(3, -3)),
        Particle2D(Vector2D(6, 3), Vector2D(-1, -3)),
        Particle2D(Vector2D(10, 3), Vector2D(-1, 2)),
        Particle2D(Vector2D(2, 0), Vector2D(2, -1)),
        Particle2D(Vector2D(0, 0), Vector2D(1, 3)),
        Particle2D(Vector2D(3, 0), Vector2D(-2, -2)),
        Particle2D(Vector2D(7, 6), Vector2D(-1, -3)),
        Particle2D(Vector2D(3, 0), Vector2D(-1, -2)),
        Particle2D(Vector2D(9, 3), Vector2D(2, 3)),
        Particle2D(Vector2D(7, 3), Vector2D(-1, 2)),
        Particle2D(Vector2D(2, 4), Vector2D(2, -3)),
        Particle2D(Vector2D(9, 5), Vector2D(-3, -3)),
    ]
    num_guards_per_quadrant = sorted(
        bathroom.num_guards_per_quadrant(initial_guards, time=100)
    )
    assert num_guards_per_quadrant == [1, 1, 3, 4]
