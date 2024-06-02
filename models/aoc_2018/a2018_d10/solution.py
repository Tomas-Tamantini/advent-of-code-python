from models.common.io import InputReader
from .parser import parse_moving_particles
from .moving_particles import MovingParticles


def aoc_2018_d10(input_reader: InputReader, **_) -> None:
    print("--- AOC 2018 - Day 10: The Stars Align ---")
    particles = list(parse_moving_particles(input_reader))
    moving_particles = MovingParticles(particles)
    moments = moving_particles.moments_of_bounding_box_area_increase()
    inflexion_point = next(moments) - 1
    print("Part 1: Message:")
    print(moving_particles.draw(inflexion_point))
    print(f"Part 2: Time to reach message: {inflexion_point}")
