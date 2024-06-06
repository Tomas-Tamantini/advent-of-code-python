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
    remaining_time = time_limit - current_state.timestamp
    num_inventory = current_state.inventory.resource_amount(resource_to_maximize)
    num_existing_robots = current_state.robots.resource_amount(resource_to_maximize)
    return (
        num_inventory
        + num_existing_robots * remaining_time
        + (remaining_time * (remaining_time - 1)) // 2
    )
