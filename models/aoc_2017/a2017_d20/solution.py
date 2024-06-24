from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_particles
from .particle_collider import ParticleCollider


def aoc_2017_d20(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2017, 20, "Particle Swarm")
    io_handler.output_writer.write_header(problem_id)
    particles = list(parse_particles(io_handler.input_reader))
    collider = ParticleCollider(particles)
    closest_to_origin = collider.particle_closest_to_origin_long_term()
    yield ProblemSolution(
        problem_id, f"Particle closest to origin: {closest_to_origin.id}", part=1
    )

    destroyed = collider.particles_destroyed_in_collisions()
    num_remaining = len(particles) - len(destroyed)
    yield ProblemSolution(problem_id, f"Particles remaining: {num_remaining}", part=1)
