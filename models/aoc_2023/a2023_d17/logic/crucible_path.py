from typing import Iterator

from models.common.graphs import a_star
from models.common.vectors import CardinalDirection, Vector2D

from .city_map import CityMap
from .crucible import Crucible


class CruciblePath:
    def __init__(
        self,
        city_map: CityMap,
        min_steps_same_direction: int,
        max_steps_same_direction: int,
    ):
        self._city_map = city_map
        self._min_steps_same_direction = min_steps_same_direction
        self._max_steps_same_direction = max_steps_same_direction

    @staticmethod
    def inital_crucible() -> Crucible:
        return Crucible(
            position=Vector2D(0, 0), direction=None, num_steps_in_same_direction=0
        )

    def _valid_directions(self, node: Crucible) -> Iterator[CardinalDirection]:
        if node.num_steps_in_same_direction < self._max_steps_same_direction:
            yield node.direction
        if node.num_steps_in_same_direction >= self._min_steps_same_direction:
            yield node.direction.turn_left()
            yield node.direction.turn_right()

    def _new_directions(self, node: Crucible) -> Iterator[CardinalDirection]:
        if node.direction is None:
            yield from CardinalDirection
        else:
            yield from self._valid_directions(node)

    def neighbors(self, node: Crucible) -> Iterator[Crucible]:
        for new_dir in self._new_directions(node):
            new_pos = node.position.move(new_dir, y_grows_down=True)
            if self._city_map.is_within_bounds(new_pos):
                num_steps_in_same_direction = (
                    node.num_steps_in_same_direction + 1
                    if new_dir == node.direction
                    else 1
                )
                yield Crucible(new_pos, new_dir, num_steps_in_same_direction)

    def is_final_state(self, crucible: Crucible) -> bool:
        return (
            crucible.position == self._city_map.final_position
            and self._min_steps_same_direction <= crucible.num_steps_in_same_direction
        )

    def weight(self, node_a: Crucible, node_b: Crucible) -> int:
        return self._city_map.heat_loss_at(node_b.position)

    def heuristic_potential(self, node: Crucible) -> int:
        return node.position.manhattan_distance(self._city_map.final_position)

    def min_heat_loss(self) -> int:
        _, distance = a_star(
            origin=self.inital_crucible(),
            is_destination=self.is_final_state,
            graph=self,
        )
        return distance
