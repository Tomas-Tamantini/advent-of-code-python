from itertools import combinations
from typing import Iterable, Iterator

from models.common.vectors import BoundingBox, Vector2D

from .proximity_sensor import ProximitySensor


def _boundary_intersections(
    sensor_a: ProximitySensor, sensor_b: ProximitySensor
) -> Iterator[Vector2D]:
    for boundary_a in sensor_a.boundaries():
        for boundary_b in sensor_b.boundaries():
            if boundary_a.slope_upwards != boundary_b.slope_upwards:
                intersection = boundary_a.intersection(boundary_b)
                if intersection is not None:
                    yield intersection


def position_which_must_be_beacon(
    search_space: BoundingBox, sensors: Iterable[ProximitySensor]
) -> Vector2D:
    for sensor_pair in combinations(sensors, 2):
        for intersection in _boundary_intersections(*sensor_pair):
            if search_space.contains(intersection):
                if all(sensor.is_out_of_reach(intersection) for sensor in sensors):
                    return intersection
