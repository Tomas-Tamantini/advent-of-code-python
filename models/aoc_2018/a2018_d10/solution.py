from models.common.io import IOHandler, Problem
from .parser import parse_moving_particles
from .moving_particles import MovingParticles


def aoc_2018_d10(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 10, "The Stars Align")
    io_handler.output_writer.write_header(problem_id)
    particles = list(parse_moving_particles(io_handler.input_reader))
    moving_particles = MovingParticles(particles)
    moments = moving_particles.moments_of_bounding_box_area_increase()
    inflexion_point = next(moments) - 1
    print("Part 1: Message:")
    print(moving_particles.draw(inflexion_point))
    print(f"Part 2: Time to reach message: {inflexion_point}")
