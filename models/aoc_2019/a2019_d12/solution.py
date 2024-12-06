from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .moons import MoonOfJupiter, MoonSystem
from .parser import parse_3d_vectors


def aoc_2019_d12(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 12, "The N-Body Problem")
    io_handler.output_writer.write_header(problem_id)
    positions = list(parse_3d_vectors(io_handler.input_reader))
    moons = [MoonOfJupiter(pos) for pos in positions]
    system = MoonSystem(moons)
    system.multi_step(num_steps=1000)
    total_energy = sum(
        m.position.manhattan_size * m.velocity.manhattan_size for m in system.moons
    )
    yield ProblemSolution(
        problem_id, f"Total energy is {total_energy}", part=1, result=total_energy
    )

    period = system.period()
    yield ProblemSolution(
        problem_id, f"System period is {period}", part=2, result=period
    )
