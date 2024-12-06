import pytest

from ..logic import (
    Blueprint,
    MiningState,
    ResourceType,
    RobotCost,
    max_num_resource,
)


def _example_blueprint_1() -> Blueprint:
    return Blueprint(
        blueprint_id=1,
        costs=[
            RobotCost(robot_type=ResourceType.ORE, cost={ResourceType.ORE: 4}),
            RobotCost(robot_type=ResourceType.CLAY, cost={ResourceType.ORE: 2}),
            RobotCost(
                robot_type=ResourceType.OBSIDIAN,
                cost={ResourceType.ORE: 3, ResourceType.CLAY: 14},
            ),
            RobotCost(
                robot_type=ResourceType.GEODE,
                cost={ResourceType.ORE: 2, ResourceType.OBSIDIAN: 7},
            ),
        ],
    )


def _example_blueprint_2() -> Blueprint:
    return Blueprint(
        blueprint_id=2,
        costs=[
            RobotCost(robot_type=ResourceType.ORE, cost={ResourceType.ORE: 2}),
            RobotCost(robot_type=ResourceType.CLAY, cost={ResourceType.ORE: 3}),
            RobotCost(
                robot_type=ResourceType.OBSIDIAN,
                cost={ResourceType.ORE: 3, ResourceType.CLAY: 8},
            ),
            RobotCost(
                robot_type=ResourceType.GEODE,
                cost={ResourceType.ORE: 3, ResourceType.OBSIDIAN: 12},
            ),
        ],
    )


@pytest.mark.parametrize(
    ("blueprint", "max_num_geodes"),
    [
        (_example_blueprint_1(), 9),
        (_example_blueprint_2(), 12),
    ],
)
def test_maximum_number_of_geodes_for_given_blueprint_is_found(
    blueprint, max_num_geodes
):
    starting_state = MiningState(inventory=dict(), fleet_size={ResourceType.ORE: 1})
    time_limit = 24
    resource_to_maximize = ResourceType.GEODE
    assert (
        max_num_resource(resource_to_maximize, time_limit, blueprint, starting_state)
        == max_num_geodes
    )
