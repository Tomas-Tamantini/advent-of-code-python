from models.common.io import (
    IOHandler,
    Problem,
    ProblemSolution,
    CharacterGrid,
    render_frame,
)
from .octopus_flash import OctopusesFlashes


def aoc_2021_d11(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 11, "Dumbo Octopus")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    octopuses = OctopusesFlashes(
        energy_levels={pos: int(height) for pos, height in grid.tiles.items()}
    )
    octopuses.multi_step(num_steps=100)
    solution = ProblemSolution(
        problem_id,
        f"The number of flashes after 100 steps is {octopuses.num_flashes}",
        part=1,
    )
    io_handler.output_writer.write_solution(solution)

    octopuses = OctopusesFlashes(
        energy_levels={pos: int(height) for pos, height in grid.tiles.items()}
    )
    current_step = 0
    while not octopuses.all_octopuses_flashed_last_step:
        current_step += 1
        octopuses.step()
        if io_handler.execution_flags.animate:
            frame = octopuses.render() + f"\nStep: {current_step}"
            render_frame(frame, sleep_seconds=0.05)
    solution = ProblemSolution(
        problem_id,
        f"The number of steps until all octopuses flash is {current_step}",
        part=2,
        supports_animation=True,
    )
    io_handler.output_writer.write_solution(solution)
