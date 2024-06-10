from typing import Iterator
from .resource_type import ResourceType
from .resource_quantity import ResourceQuantity


class Blueprint:
    def __init__(self, blueprint_id: int, costs: dict[ResourceType, ResourceQuantity]):
        self._id = blueprint_id
        self._costs = costs

    @property
    def blueprint_id(self) -> int:
        return self._id

    def cost_to_build_robot(
        self, robot_resource_type: ResourceType
    ) -> ResourceQuantity:
        return self._costs[robot_resource_type]

    def robots_that_can_be_built(
        self, inventory: ResourceQuantity
    ) -> Iterator[ResourceType]:
        for robot_type in ResourceType:
            if robot_type in self._costs and self._costs[robot_type].all_resources_leq(
                inventory
            ):
                yield robot_type

    def max_fraction_of_robot_that_can_be_built(
        self, robot_resource_type: ResourceType, inventory: ResourceQuantity
    ) -> float:
        fraction = 1.0
        cost = self._costs[robot_resource_type]
        for resource, quantity in cost.resource_amounts():
            if quantity > 0:
                fraction = min(fraction, inventory.resource_amount(resource) / quantity)
        return fraction
