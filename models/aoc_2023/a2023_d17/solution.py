from typing import Iterator

from models.common.io import CharacterGrid, IOHandler, Problem, ProblemSolution

from .logic import CityMap, CruciblePath


def aoc_2023_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 17, "Clumsy Crucible")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    city_map = CityMap(grid)

    light_crucible = CruciblePath(
        city_map, min_steps_same_direction=0, max_steps_same_direction=3
    )
    io_handler.output_writer.give_time_estimation("10s", part=1)
    light_heat_loss = light_crucible.min_heat_loss()
    yield ProblemSolution(
        problem_id,
        f"Minimum heat loss for light crucible is {light_heat_loss}",
        result=light_heat_loss,
        part=1,
    )

    ultra_crucible = CruciblePath(
        city_map, min_steps_same_direction=4, max_steps_same_direction=10
    )
    io_handler.output_writer.give_time_estimation("20s", part=2)
    ultra_heat_loss = ultra_crucible.min_heat_loss()
    yield ProblemSolution(
        problem_id,
        f"Minimum heat loss for ultra crucible is {ultra_heat_loss}",
        result=ultra_heat_loss,
        part=2,
    )
