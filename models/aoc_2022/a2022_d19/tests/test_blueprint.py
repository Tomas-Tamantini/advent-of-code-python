from ..logic import ResourceType, RobotCost, Blueprint


def test_blueprint_informs_how_much_of_given_resource_it_costs_to_build_given_robot():
    blueprint = Blueprint(
        blueprint_id=1,
        costs=(
            RobotCost(
                robot_type=ResourceType.ORE,
                cost={ResourceType.ORE: 1, ResourceType.CLAY: 2},
            ),
            RobotCost(
                robot_type=ResourceType.CLAY,
                cost={ResourceType.ORE: 3, ResourceType.CLAY: 4},
            ),
        ),
    )
    assert (
        blueprint.cost(
            robot_type=ResourceType.CLAY,
            resource_type=ResourceType.ORE,
        )
        == 3
    )

    assert (
        blueprint.cost(
            robot_type=ResourceType.ORE,
            resource_type=ResourceType.OBSIDIAN,
        )
        == 0
    )
