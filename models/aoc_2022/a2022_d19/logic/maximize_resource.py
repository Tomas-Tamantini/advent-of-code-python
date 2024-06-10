from typing import Iterator
from .resource_type import ResourceType
from .blueprint import Blueprint
from .mining_state import MiningState


def max_num_resource(
    resource_to_maximize: ResourceType,
    time_limit: int,
    blueprint: Blueprint,
    initial_state: MiningState,
) -> int:
    explored_states = set()
    explore_stack = [initial_state]
    max_resources = 0
    while explore_stack:
        current_state = explore_stack.pop()
        if current_state in explored_states:
            continue
        explored_states.add(current_state)
        # Branch and bound
        if (
            _resource_upper_limit(
                resource_to_maximize, time_limit, blueprint, current_state
            )
            > max_resources
        ):
            max_resources = max(
                max_resources,
                current_state.inventory.resource_amount(resource_to_maximize),
            )
            if current_state.timestamp < time_limit:
                for next_state in current_state.next_states(blueprint):
                    explore_stack.append(next_state)
    return max_resources


def _resource_upper_limit(
    resource_to_maximize: ResourceType,
    time_limit: int,
    blueprint: Blueprint,
    current_state: MiningState,
) -> int:
    if time_limit == current_state.timestamp:
        return current_state.inventory.resource_amount(resource_to_maximize)
    remaining_factory_capacity: float = 1.0
    new_inventory = current_state.inventory
    new_robots = current_state.robots
    for robot_type in _prioritized_robots(
        resource_to_maximize, blueprint, current_state
    ):
        robot_fraction = min(
            remaining_factory_capacity,
            blueprint.max_fraction_of_robot_that_can_be_built(
                robot_type, new_inventory
            ),
        )
        new_robots = new_robots.increment_resource(robot_type, robot_fraction)
        new_inventory = new_inventory - robot_fraction * blueprint.cost_to_build_robot(
            robot_type
        )
        remaining_factory_capacity -= robot_fraction
    new_inventory = new_inventory + current_state.robots
    new_timestamp = current_state.timestamp + 1
    new_state = MiningState(new_timestamp, new_inventory, new_robots)
    return _resource_upper_limit(resource_to_maximize, time_limit, blueprint, new_state)


def _prioritized_robots(
    resource_to_maximize: ResourceType,
    blueprint: Blueprint,
    current_state: MiningState,
) -> Iterator[ResourceType]:
    # TODO: Implement a better heuristic for robot prioritization
    yield from (
        ResourceType.GEODE,
        ResourceType.OBSIDIAN,
        ResourceType.CLAY,
        ResourceType.ORE,
    )
