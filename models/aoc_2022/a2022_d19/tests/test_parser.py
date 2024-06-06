from models.common.io import InputFromString
from ..parser import parse_blueprints
from ..logic import ResourceType, ResourceQuantity


def test_parse_blueprints():
    input_str = """
    Blueprint 1: Each ore robot costs 2 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 15 clay. Each geode robot costs 2 ore and 15 obsidian.
    Blueprint 2: Each ore robot costs 4 ore. Each clay robot costs 4 ore. Each obsidian robot costs 4 ore and 12 clay. Each geode robot costs 3 ore and 8 obsidian.
    """

    blueprints = list(parse_blueprints(InputFromString(input_str)))
    assert len(blueprints) == 2
    assert blueprints[0].blueprint_id == 1
    assert blueprints[1].blueprint_id == 2
    assert blueprints[0].cost_to_build_robot(ResourceType.ORE) == ResourceQuantity(
        {ResourceType.ORE: 2}
    )
    assert blueprints[1].cost_to_build_robot(ResourceType.GEODE) == ResourceQuantity(
        {ResourceType.ORE: 3, ResourceType.OBSIDIAN: 8}
    )
