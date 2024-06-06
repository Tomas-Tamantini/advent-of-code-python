from ..logic import ResourceType, ResourceQuantity, Blueprint


def test_blueprint_informs_the_cost_of_building_given_robot():
    blueprint = Blueprint(
        blueprint_id=1,
        costs={
            ResourceType.ORE: ResourceQuantity(
                {ResourceType.ORE: 1, ResourceType.CLAY: 2}
            ),
            ResourceType.CLAY: ResourceQuantity(
                {ResourceType.ORE: 3, ResourceType.CLAY: 4}
            ),
        },
    )
    assert blueprint.cost_to_build_robot(
        robot_resource_type=ResourceType.ORE
    ) == ResourceQuantity(
        {
            ResourceType.ORE: 1,
            ResourceType.CLAY: 2,
        }
    )


def test_blueprint_informs_the_robots_that_can_be_built_given_resources():
    inventory = ResourceQuantity(
        {ResourceType.ORE: 10, ResourceType.CLAY: 3, ResourceType.OBSIDIAN: 2}
    )
    blueprint = Blueprint(
        blueprint_id=1,
        costs={
            ResourceType.ORE: ResourceQuantity(
                {ResourceType.ORE: 1, ResourceType.CLAY: 2}
            ),
            ResourceType.CLAY: ResourceQuantity(
                {ResourceType.ORE: 3, ResourceType.CLAY: 4}
            ),
            ResourceType.GEODE: ResourceQuantity({ResourceType.OBSIDIAN: 2}),
        },
    )
    assert set(blueprint.robots_that_can_be_built(inventory)) == {
        ResourceType.ORE,
        ResourceType.GEODE,
    }
