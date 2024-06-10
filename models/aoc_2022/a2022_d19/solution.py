from models.common.io import InputReader, ProgressBarConsole
from .parser import parse_blueprints
from .logic import max_num_resource, ResourceType, ResourceQuantity, MiningState


def aoc_2022_d19(
    input_reader: InputReader, progress_bar: ProgressBarConsole, **_
) -> None:
    print("--- AOC 2022 - Day 19: Not Enough Minerals ---")
    blueprints = list(parse_blueprints(input_reader))
    time_limit = 24
    resource_to_maximize = ResourceType.GEODE
    initial_state = MiningState(
        timestamp=0,
        inventory=ResourceQuantity(dict()),
        robots=ResourceQuantity({ResourceType.ORE: 1}),
    )

    sum_quality_levels = 0
    progress_bar.update(step=0, expected_num_steps=len(blueprints))
    for i, blueprint in enumerate(blueprints):
        blueprint_id = blueprint.blueprint_id
        num_geodes = max_num_resource(
            resource_to_maximize, time_limit, blueprint, initial_state
        )
        quality_level = blueprint_id * num_geodes
        sum_quality_levels += quality_level
        progress_bar.update(step=i + 1, expected_num_steps=len(blueprints))
    print(
        f"Part 1: The sum of quality levels for all blueprints is {sum_quality_levels}"
    )

    time_limit = 32
    geode_product = 1
    progress_bar.update(step=0, expected_num_steps=3)
    for i, blueprint in enumerate(blueprints[:3]):
        num_geodes = max_num_resource(
            resource_to_maximize, time_limit, blueprint, initial_state
        )
        geode_product *= num_geodes
        progress_bar.update(step=i + 1, expected_num_steps=3)
    print(f"Part 2: The product of the number of geodes is {geode_product}")
