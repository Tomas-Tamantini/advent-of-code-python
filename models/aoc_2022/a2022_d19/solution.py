from models.common.io import InputReader
from .parser import parse_blueprints
from .logic import max_num_resource, ResourceType, ResourceQuantity, MiningState


def aoc_2022_d19(input_reader: InputReader, **_) -> None:
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
    for blueprint in blueprints:
        blueprint_id = blueprint.blueprint_id
        num_geodes = max_num_resource(
            resource_to_maximize, time_limit, blueprint, initial_state
        )
        quality_level = blueprint_id * num_geodes
        sum_quality_levels += quality_level

    print(
        f"Part 1: The sum of quality levels for all blueprints is {sum_quality_levels}"
    )
