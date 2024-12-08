from typing import Iterator

from models.common.optimization.linear_programming import Constraint, ConstraintType

from ..blueprint import Blueprint
from ..mining_state import MiningState
from ..resource_type import ResourceType
from .variables import VariableClass, VariableId


def constraints(
    time_limit: int,
    blueprint: Blueprint,
    initial_state: MiningState,
) -> Iterator[Constraint]:
    yield from _initial_inventory_given(initial_state)
    yield from _initial_fleet_size_given(initial_state)
    yield from _robot_fleet_growth(time_limit)
    yield from _inventory_growth(time_limit, blueprint)
    yield from _max_one_robot_built_per_minute(time_limit)
    yield from _robot_only_built_if_enough_resources(time_limit, blueprint)


def _initial_inventory_given(initial_state: MiningState) -> Iterator[Constraint]:
    for resource_type in ResourceType:
        var_id = VariableId(VariableClass.RESOURCE_AMOUNT, resource_type, minute=1)
        coefficients = {var_id: 1}
        resource_amount = initial_state.resource_amount(resource_type)
        yield Constraint(
            coefficients,
            right_hand_side=resource_amount,
            constraint_type=ConstraintType.EQUAL,
            description=(
                f"Initial amount of resource {resource_type} is {resource_amount}"
            ),
        )


def _initial_fleet_size_given(initial_state: MiningState) -> Iterator[Constraint]:
    for resource_type in ResourceType:
        var_id = VariableId(VariableClass.FLEET_SIZE, resource_type, minute=1)
        coefficients = {var_id: 1}
        num_robots = initial_state.num_robots(resource_type)
        yield Constraint(
            coefficients,
            right_hand_side=num_robots,
            constraint_type=ConstraintType.EQUAL,
            description=(
                f"Initial fleet size for resource {resource_type} is {num_robots}"
            ),
        )


def _robot_fleet_growth(time_limit: int) -> Iterator[Constraint]:
    for resource_type in ResourceType:
        for minute in range(2, time_limit + 2):
            id_current_fleet = VariableId(
                VariableClass.FLEET_SIZE, resource_type, minute
            )
            id_previous_fleet = VariableId(
                VariableClass.FLEET_SIZE, resource_type, minute - 1
            )
            id_previous_build = VariableId(
                VariableClass.BUILD_DECISION, resource_type, minute - 1
            )
            coefficients = {
                id_current_fleet: 1,
                id_previous_fleet: -1,
                id_previous_build: -1,
            }
            yield Constraint(
                coefficients,
                right_hand_side=0,
                constraint_type=ConstraintType.EQUAL,
                description=(
                    f"Fleet size for robot type {resource_type} "
                    f"for minute {minute} increments from previous minute"
                ),
            )


def _inventory_growth(time_limit: int, blueprint: Blueprint) -> Iterator[Constraint]:
    for resource_type in ResourceType:
        for minute in range(2, time_limit + 2):
            id_current_inventory = VariableId(
                VariableClass.RESOURCE_AMOUNT, resource_type, minute
            )
            id_previous_inventory = VariableId(
                VariableClass.RESOURCE_AMOUNT, resource_type, minute - 1
            )
            id_previous_fleet = VariableId(
                VariableClass.FLEET_SIZE, resource_type, minute - 1
            )
            coefficients = {
                id_current_inventory: 1,
                id_previous_inventory: -1,
                id_previous_fleet: -1,
            }
            for robot_type in ResourceType:
                id_previous_build = VariableId(
                    VariableClass.BUILD_DECISION, robot_type, minute - 1
                )
                coefficients[id_previous_build] = blueprint.cost(
                    robot_type, resource_type
                )
            yield Constraint(
                coefficients,
                right_hand_side=0,
                constraint_type=ConstraintType.EQUAL,
                description=(
                    f"Inventory of resource {resource_type} "
                    f"at the start of minute {minute} increments from previous minute"
                ),
            )


def _max_one_robot_built_per_minute(time_limit: int) -> Iterator[Constraint]:
    for minute in range(1, time_limit + 1):
        coefficients = dict()
        for r in ResourceType:
            id_build = VariableId(VariableClass.BUILD_DECISION, r, minute)
            coefficients[id_build] = 1
        yield Constraint(
            coefficients,
            right_hand_side=1,
            constraint_type=ConstraintType.LESS_THAN_OR_EQUAL,
            description=f"At most one robot can be built on minute {minute}",
        )


def _robot_only_built_if_enough_resources(
    time_limit: int, blueprint: Blueprint
) -> Iterator[Constraint]:
    for resource_type in ResourceType:
        for minute in range(1, time_limit + 1):
            inventory_index = VariableId(
                VariableClass.RESOURCE_AMOUNT, resource_type, minute
            )
            coefficients = {inventory_index: -1}
            for robot_type in ResourceType:
                id_build = VariableId(VariableClass.BUILD_DECISION, robot_type, minute)
                coefficients[id_build] = blueprint.cost(robot_type, resource_type)
            yield Constraint(
                coefficients,
                right_hand_side=0,
                constraint_type=ConstraintType.LESS_THAN_OR_EQUAL,
                description=(
                    f"Robot of type {resource_type} "
                    f"built on minute {minute} must be within budget"
                ),
            )
