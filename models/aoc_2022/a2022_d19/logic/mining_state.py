from dataclasses import dataclass

from .resource_type import ResourceType


@dataclass
class MiningState:
    inventory: dict[ResourceType, int]
    fleet_size: dict[ResourceType, int]

    def resource_amount(self, resource_type: ResourceType) -> int:
        return self.inventory.get(resource_type, 0)

    def num_robots(self, resource_type: ResourceType) -> int:
        return self.fleet_size.get(resource_type, 0)
