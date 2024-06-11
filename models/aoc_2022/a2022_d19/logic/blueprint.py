from typing import Iterable
from .resource_type import ResourceType
from .robot_cost import RobotCost


class Blueprint:
    def __init__(self, blueprint_id: int, costs: Iterable[RobotCost]):
        self._id = blueprint_id
        self._costs = {robot_cost.robot_type: robot_cost.cost for robot_cost in costs}

    @property
    def blueprint_id(self) -> int:
        return self._id

    def cost(self, robot_type: ResourceType, resource_type: ResourceType) -> int:
        return self._costs.get(robot_type, {}).get(resource_type, 0)
