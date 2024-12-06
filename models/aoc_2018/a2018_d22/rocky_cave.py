from dataclasses import dataclass
from enum import Enum
from typing import Iterator, Optional

from models.common.graphs import a_star
from models.common.vectors import BoundingBox, CardinalDirection, Vector2D


class _RegionType(int, Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


class _Gear(int, Enum):
    NEITHER = 0
    TORCH = 1
    CLIMBING_GEAR = 2


class RockyCave:
    def __init__(
        self,
        depth: int,
        target: Vector2D,
        row_multiplier: int,
        col_multiplier: int,
        erosion_level_mod: int,
    ) -> None:
        self._depth = depth
        self._target = target
        self._row_multiplier = row_multiplier
        self._col_multiplier = col_multiplier
        self._erosion_level_mod = erosion_level_mod
        self._erosion_levels: dict[Vector2D, int] = dict()

    @property
    def target(self) -> Vector2D:
        return self._target

    def erosion_level(self, pos: Vector2D) -> int:
        if pos in self._erosion_levels:
            return self._erosion_levels[pos]
        if pos == Vector2D(0, 0) or pos == self._target:
            geo_index = 0
        elif pos.y == 0:
            geo_index = pos.x * self._row_multiplier
        elif pos.x == 0:
            geo_index = pos.y * self._col_multiplier
        else:
            geo_index = self.erosion_level(
                pos.move(CardinalDirection.WEST)
            ) * self.erosion_level(pos.move(CardinalDirection.SOUTH))
        level = (geo_index + self._depth) % self._erosion_level_mod
        self._erosion_levels[pos] = level
        return level

    def region_type(self, pos: Vector2D) -> _RegionType:
        return _RegionType(self.erosion_level(pos) % 3)

    def risk_level(self, region: Optional[BoundingBox] = None) -> int:
        if region is None:
            region = BoundingBox(
                bottom_left=Vector2D(0, 0),
                top_right=self._target,
            )
        return sum(
            self.region_type(Vector2D(x, y))
            for x in range(region.bottom_left.x, region.top_right.x + 1)
            for y in range(region.bottom_left.y, region.top_right.y + 1)
        )


@dataclass(frozen=True, order=True)
class _ExplorerState:
    position: Vector2D
    gear: _Gear


class CaveExplorer:
    def __init__(
        self, cave: RockyCave, time_to_move: int, time_to_switch_gear: int
    ) -> None:
        self._cave = cave
        self._time_to_move = time_to_move
        self._time_to_switch_gear = time_to_switch_gear

    @staticmethod
    def _is_out_of_bounds(position: Vector2D) -> bool:
        return position.x < 0 or position.y < 0

    def neighbors(self, node: _ExplorerState) -> Iterator[_ExplorerState]:
        allowed_gears = {
            _RegionType.ROCKY: {_Gear.TORCH, _Gear.CLIMBING_GEAR},
            _RegionType.WET: {_Gear.NEITHER, _Gear.CLIMBING_GEAR},
            _RegionType.NARROW: {_Gear.NEITHER, _Gear.TORCH},
        }
        for adjacent_position in node.position.adjacent_positions():
            if self._is_out_of_bounds(adjacent_position):
                continue
            adjacent_region = self._cave.region_type(adjacent_position)
            if node.gear in allowed_gears[adjacent_region]:
                yield _ExplorerState(
                    position=adjacent_position,
                    gear=node.gear,
                )
        for gear in allowed_gears[self._cave.region_type(node.position)]:
            if gear != node.gear:
                yield _ExplorerState(
                    position=node.position,
                    gear=gear,
                )

    def weight(self, node_a: _ExplorerState, node_b: _ExplorerState) -> int:
        if node_a.position != node_b.position:
            return self._time_to_move
        return self._time_to_switch_gear

    def heuristic_potential(self, node: _ExplorerState) -> int:
        return node.position.manhattan_distance(self._cave.target)

    def shortest_time_to_target(self) -> int:
        initial_state = _ExplorerState(position=Vector2D(0, 0), gear=_Gear.TORCH)
        final_state = _ExplorerState(position=self._cave.target, gear=_Gear.TORCH)
        _, distance = a_star(
            origin=initial_state,
            is_destination=lambda state: state == final_state,
            graph=self,
        )
        return distance
