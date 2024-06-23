from models.common.io import IOHandler
from .parser import parse_3d_vectors
from .moons import MoonOfJupiter, MoonSystem


def aoc_2019_d12(io_handler: IOHandler) -> None:
    print("--- AOC 2019 - Day 12: The N-Body Problem ---")
    positions = list(parse_3d_vectors(io_handler.input_reader))
    moons = [MoonOfJupiter(pos) for pos in positions]
    system = MoonSystem(moons)
    system.multi_step(num_steps=1000)
    total_energy = sum(
        m.position.manhattan_size * m.velocity.manhattan_size for m in system.moons
    )
    print(f"Part 1: Total energy is {total_energy}")
    period = system.period()
    print(f"Part 2: System period is {period}")
