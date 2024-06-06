import pytest
from ..logic import (
    ResourceType,
    ResourceQuantity,
    Blueprint,
    MiningState,
    max_num_resource,
)


def _example_blueprint_1() -> Blueprint:
    return Blueprint(
        blueprint_id=1,
        costs={
            ResourceType.ORE: ResourceQuantity({ResourceType.ORE: 4}),
            ResourceType.CLAY: ResourceQuantity({ResourceType.ORE: 2}),
            ResourceType.OBSIDIAN: ResourceQuantity(
                {ResourceType.ORE: 3, ResourceType.CLAY: 14}
            ),
            ResourceType.GEODE: ResourceQuantity(
                {ResourceType.ORE: 2, ResourceType.OBSIDIAN: 7}
            ),
        },
    )


def _example_blueprint_2() -> Blueprint:
    return Blueprint(
        blueprint_id=2,
        costs={
            ResourceType.ORE: ResourceQuantity({ResourceType.ORE: 2}),
            ResourceType.CLAY: ResourceQuantity({ResourceType.ORE: 3}),
            ResourceType.OBSIDIAN: ResourceQuantity(
                {ResourceType.ORE: 3, ResourceType.CLAY: 8}
            ),
            ResourceType.GEODE: ResourceQuantity(
                {ResourceType.ORE: 3, ResourceType.OBSIDIAN: 12}
            ),
        },
    )


@pytest.mark.parametrize(
    "blueprint, max_num_geodes",
    [
        (_example_blueprint_1(), 9),
        (_example_blueprint_2(), 12),
    ],
)
def test_maximum_number_of_geodes_for_given_blueprint_is_found(
    blueprint, max_num_geodes
):
    starting_state = MiningState(
        timestamp=0,
        inventory=ResourceQuantity(dict()),
        robots=ResourceQuantity({ResourceType.ORE: 1}),
    )
    time_limit = 24
    resource_to_maximize = ResourceType.GEODE
    assert (
        max_num_resource(resource_to_maximize, time_limit, blueprint, starting_state)
        == max_num_geodes
    )
