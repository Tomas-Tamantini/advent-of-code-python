from models.common.vectors import BoundingBox, Vector2D

from ..moving_particles import MovingParticle, MovingParticles


def test_can_query_particle_position_at_given_time():
    particle = MovingParticle(
        position=Vector2D(10, 20),
        velocity=Vector2D(2, 3),
    )
    assert particle.position_at_time(0) == Vector2D(10, 20)
    assert particle.position_at_time(1) == Vector2D(12, 23)
    assert particle.position_at_time(2) == Vector2D(14, 26)


def test_bounding_box_of_moving_particles_is_dynamic():
    moving_particles = MovingParticles(
        particles=(
            MovingParticle(position=Vector2D(0, 0), velocity=Vector2D(1, 1)),
            MovingParticle(position=Vector2D(10, 0), velocity=Vector2D(2, 1)),
            MovingParticle(position=Vector2D(0, 10), velocity=Vector2D(1, 3)),
        )
    )
    assert moving_particles.bounding_box_at_time(0) == BoundingBox(
        Vector2D(0, 0), Vector2D(10, 10)
    )
    assert moving_particles.bounding_box_at_time(1) == BoundingBox(
        Vector2D(1, 1), Vector2D(12, 13)
    )
    assert moving_particles.bounding_box_at_time(2) == BoundingBox(
        Vector2D(2, 2), Vector2D(14, 16)
    )


def test_particles_can_be_converted_to_string():
    moving_particles = MovingParticles(
        particles=(
            MovingParticle(position=Vector2D(100, 100), velocity=Vector2D(1, 1)),
            MovingParticle(position=Vector2D(101, 101), velocity=Vector2D(2, 1)),
        )
    )
    assert moving_particles.draw(time=1) == "#..\n..#"


def test_can_iterate_through_moments_when_bounding_box_area_is_increasing():
    moving_particles = MovingParticles(
        particles=(
            MovingParticle(position=Vector2D(0, 0), velocity=Vector2D(0, 0)),
            MovingParticle(position=Vector2D(5, 5), velocity=Vector2D(0, -1)),
        )
    )
    moments = moving_particles.moments_of_bounding_box_area_increase()
    assert next(moments) == 6
    assert next(moments) == 7
    assert next(moments) == 8
