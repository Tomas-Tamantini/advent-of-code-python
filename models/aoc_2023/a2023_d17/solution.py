from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution, CharacterGrid
from .logic import CityMap, CruciblePath


def aoc_2023_d17(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2023, 17, "Clumsy Crucible")
    io_handler.output_writer.write_header(problem_id)
    grid = CharacterGrid(io_handler.input_reader.read())
    city_map = CityMap(grid)

    light_crucible = CruciblePath(
        city_map, min_steps_same_direction=0, max_steps_same_direction=3
    )
    light_heat_loss = light_crucible.min_heat_loss()
    yield ProblemSolution(
        problem_id,
        f"Minimum heat loss for light crucible is {light_heat_loss}",
        result=light_heat_loss,
        part=1,
    )

    # TODO: Find out why it's giving the wrong answer (995 vs the correct 982)
    # ultra_crucible = CruciblePath(
    #     city_map, min_steps_same_direction=4, max_steps_same_direction=10
    # )
    # ultra_heat_loss = ultra_crucible.min_heat_loss()
    # yield ProblemSolution(
    #     problem_id,
    #     f"Minimum heat loss for ultra crucible is {ultra_heat_loss}",
    #     result=ultra_heat_loss,
    #     part=2,
    # )
