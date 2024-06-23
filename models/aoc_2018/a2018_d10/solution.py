from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_moving_particles
from .moving_particles import MovingParticles


def aoc_2018_d10(io_handler: IOHandler) -> None:
    problem_id = Problem(2018, 10, "The Stars Align")
    io_handler.output_writer.write_header(problem_id)
    particles = list(parse_moving_particles(io_handler.input_reader))
    moving_particles = MovingParticles(particles)
    moments = moving_particles.moments_of_bounding_box_area_increase()
    inflexion_point = next(moments) - 1
    solution = ProblemSolution(
        problem_id, f"Message:\n{moving_particles.draw(inflexion_point)}", part=1
    )
    io_handler.output_writer.write_solution(solution)
    solution = ProblemSolution(
        problem_id, f"Time to reach message: {inflexion_point}", part=2
    )
    io_handler.output_writer.write_solution(solution)
