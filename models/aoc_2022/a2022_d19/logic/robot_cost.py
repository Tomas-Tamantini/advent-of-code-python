from dataclasses import dataclass
from .resource_type import ResourceType


@dataclass
class RobotCost:
    robot_type: ResourceType
    cost: dict[ResourceType, int]
