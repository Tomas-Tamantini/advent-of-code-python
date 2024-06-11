from typing import Iterator, Iterable
from models.common.io import InputReader
from .logic import Blueprint, ResourceType, RobotCost

STR_TO_RESOURCE_TYPE = {
    "ore": ResourceType.ORE,
    "clay": ResourceType.CLAY,
    "obsidian": ResourceType.OBSIDIAN,
    "geode": ResourceType.GEODE,
}


def _parse_robot_cost(cost_str: str) -> dict[ResourceType, int]:
    resources_str = cost_str.split("costs")[1].strip()
    robot_cost = dict()
    for resource_str in resources_str.split("and"):
        resource_parts = resource_str.strip().split(" ")
        resource = STR_TO_RESOURCE_TYPE[resource_parts[1].strip()]
        resource_quantity = int(resource_parts[0])
        robot_cost[resource] = resource_quantity
    return robot_cost


def _parse_robot_costs(robots: Iterable[str]) -> Iterator[RobotCost]:
    for robot in robots:
        robot = robot.strip()
        if robot:
            robot_type = STR_TO_RESOURCE_TYPE[robot.split(" ")[1]]
            robot_cost = _parse_robot_cost(robot)
            yield RobotCost(robot_type, robot_cost)


def _parse_blueprint(line: str) -> Blueprint:
    parts = line.split(":")
    blueprint_id = int(parts[0].strip().split(" ")[1])
    costs = _parse_robot_costs(parts[1].split("."))
    return Blueprint(blueprint_id, costs)


def parse_blueprints(input_reader: InputReader) -> Iterator[Blueprint]:
    for line in input_reader.read_stripped_lines():
        yield _parse_blueprint(line)
