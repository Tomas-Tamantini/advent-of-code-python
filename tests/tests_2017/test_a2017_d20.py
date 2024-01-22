from models.aoc_2017 import Particle, ParticleCollider


def test_particle_which_stays_closest_to_origin_long_term_is_the_one_with_smallest_manhattan_acceleration():
    particle_a = Particle(
        id=0,
        position=(1000, 2000, 3000),
        velocity=(300, 400, 500),
        acceleration=(-1, 4, 0),
    )
    particle_b = Particle(
        id=1,
        position=(0, 0, 0),
        velocity=(0, 0, 0),
        acceleration=(1, 2, -3),
    )
    collider = ParticleCollider([particle_a, particle_b])
    assert collider.particle_closest_to_origin_long_term() == particle_a


def test_particles_which_never_collide_return_no_collision():
    particle_a = Particle(
        id=0,
        position=(3, 0, 0),
        velocity=(2, 0, 0),
        acceleration=(-1, 0, 0),
    )
    particle_b = Particle(
        id=1,
        position=(4, 1, 0),
        velocity=(2, 0, 0),
        acceleration=(1, 0, 0),
    )
    collider = ParticleCollider([particle_a, particle_b])
    assert collider.particles_destroyed_in_collisions() == set()


def test_particles_which_collided_in_the_past_return_no_collision():
    particle_a = Particle(
        id=0,
        position=(1, 0, 0),
        velocity=(1, 0, 0),
        acceleration=(0, 0, 0),
    )
    particle_b = Particle(
        id=1,
        position=(0, 0, 1),
        velocity=(0, 0, 1),
        acceleration=(0, 0, 0),
    )
    collider = ParticleCollider([particle_a, particle_b])
    assert collider.particles_destroyed_in_collisions() == set()


def test_particles_which_will_collide_in_the_future_return_a_collision():
    particle_a = Particle(
        id=0,
        position=(-3, 1, 2),
        velocity=(2, 3, -1),
        acceleration=(1, 2, 1),
    )
    particle_b = Particle(
        id=1,
        position=(-2, 2, 2),
        velocity=(0, 2, 1),
        acceleration=(2, 2, -1),
    )
    collider = ParticleCollider([particle_a, particle_b])
    assert collider.particles_destroyed_in_collisions() == {particle_a, particle_b}


def test_particles_destroyed_in_collision_do_not_collide_with_others_after_that():
    particle_a = Particle(
        id=0,
        position=(-6, 0, 0),
        velocity=(3, 0, 0),
        acceleration=(0, 0, 0),
    )
    particle_b = Particle(
        id=1,
        position=(-4, 0, 0),
        velocity=(2, 0, 0),
        acceleration=(0, 0, 0),
    )
    particle_c = Particle(
        id=2,
        position=(-2, 0, 0),
        velocity=(1, 0, 0),
        acceleration=(0, 0, 0),
    )
    particle_d = Particle(
        id=3,
        position=(0, 0, 0),
        velocity=(1, 0, 0),
        acceleration=(0, 0, 0),
    )
    collider = ParticleCollider([particle_a, particle_b, particle_c, particle_d])
    assert collider.particles_destroyed_in_collisions() == {
        particle_a,
        particle_b,
        particle_c,
    }
