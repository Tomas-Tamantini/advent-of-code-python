from models.common.io import IOHandler
from .parser import parse_blueprints
from .logic import max_num_resource, ResourceType, MiningState

# See MILP modelling at - https://colab.research.google.com/drive/1eD3sn1LPaT_qwa1PSUpPvhJopiWKPKGy?usp=sharing


def aoc_2022_d19(io_handler: IOHandler) -> None:
    print("--- AOC 2022 - Day 19: Not Enough Minerals ---")
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
    print(
        f"Part 1: The sum of quality levels for all blueprints is {sum_quality_levels}"
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
    print(f"Part 2: The product of the number of geodes is {geode_product}")
