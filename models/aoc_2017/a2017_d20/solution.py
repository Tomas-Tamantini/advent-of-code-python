from models.common.io import InputReader
from .parser import parse_particles
from .particle_collider import ParticleCollider


def aoc_2017_d20(input_reader: InputReader, **_) -> None:
    print("--- AOC 2017 - Day 20: Particle Swarm ---")
    particles = list(parse_particles(input_reader))
    collider = ParticleCollider(particles)
    closest_to_origin = collider.particle_closest_to_origin_long_term()
    print(f"Part 1: Particle closest to origin: {closest_to_origin.id}")
    destroyed = collider.particles_destroyed_in_collisions()
    num_remaining = len(particles) - len(destroyed)
    print(f"Part 1: Particles remaining: {num_remaining}")
