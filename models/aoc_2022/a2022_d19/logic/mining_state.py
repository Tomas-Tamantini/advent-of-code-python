from typing import Iterator
from dataclasses import dataclass
from .resource_quantity import ResourceQuantity
from .blueprint import Blueprint


@dataclass(frozen=True)
class MiningState:
    timestamp: int
    inventory: ResourceQuantity
    robots: ResourceQuantity

    def _build_nothing(self, incremented_inventory: ResourceQuantity) -> "MiningState":
        return MiningState(
            timestamp=self.timestamp + 1,
            inventory=incremented_inventory,
            robots=self.robots,
        )

    def next_states(self, blueprint: Blueprint) -> Iterator["MiningState"]:
        incremented_inventory = self.inventory + self.robots
        yield self._build_nothing(incremented_inventory)
        for robot in blueprint.robots_that_can_be_built(incremented_inventory):
            new_robots = self.robots.increment_resource(robot)
            new_inventory = incremented_inventory - blueprint.cost_to_build_robot(robot)
            yield MiningState(
                timestamp=self.timestamp + 1, inventory=new_inventory, robots=new_robots
            )
