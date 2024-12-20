from typing import Iterator

from models.common.io import IOHandler, Problem, ProblemSolution

from .logic import MiningState, ResourceType, max_num_resource
from .parser import parse_blueprints

# See MILP modelling at - https://colab.research.google.com/drive/1eD3sn1LPaT_qwa1PSUpPvhJopiWKPKGy?usp=sharing


def aoc_2022_d19(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2022, 19, "Not Enough Minerals")
    io_handler.output_writer.write_header(problem_id)
    blueprints = list(parse_blueprints(io_handler.input_reader))
    time_limit = 24
    resource_to_maximize = ResourceType.GEODE
    initial_state = MiningState(
        inventory=dict(),
        fleet_size={ResourceType.ORE: 1},
    )

    sum_quality_levels = 0
    io_handler.progress_bar.update(step=0, expected_num_steps=len(blueprints))
    for i, blueprint in enumerate(blueprints):
        blueprint_id = blueprint.blueprint_id
        num_geodes = max_num_resource(
            resource_to_maximize, time_limit, blueprint, initial_state
        )
        quality_level = blueprint_id * num_geodes
        sum_quality_levels += quality_level
        io_handler.progress_bar.update(step=i + 1, expected_num_steps=len(blueprints))
    yield ProblemSolution(
        problem_id,
        f"The sum of quality levels for all blueprints is {sum_quality_levels}",
        part=1,
        result=sum_quality_levels,
    )

    time_limit = 32
    geode_product = 1
    io_handler.progress_bar.update(step=0, expected_num_steps=3)
    for i, blueprint in enumerate(blueprints[:3]):
        num_geodes = max_num_resource(
            resource_to_maximize, time_limit, blueprint, initial_state
        )
        geode_product *= num_geodes
        io_handler.progress_bar.update(step=i + 1, expected_num_steps=3)
    yield ProblemSolution(
        problem_id,
        f"The product of the number of geodes is {geode_product}",
        part=2,
        result=geode_product,
    )
