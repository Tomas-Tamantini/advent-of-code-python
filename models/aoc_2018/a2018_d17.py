from enum import Enum
from dataclasses import dataclass
from typing import Optional, Iterator
from models.vectors import Vector2D, BoundingBox, CardinalDirection


class _SoilType(str, Enum):
    CLAY = "#"
    FLOWING_WATER = "|"
    BOTTOM_CONFINED_WATER = "_"
    LEFT_CONFINED_WATER = "<"
    RIGHT_CONFINED_WATER = ">"
    STANDING_WATER = "~"
    SAND = "."


@dataclass(frozen=True)
class _Tile:
    position: Vector2D
    soil_type: _SoilType


@dataclass(frozen=True)
class _SoilGrouping:
    center: Optional[_SoilType] = None
    left: Optional[_SoilType] = None
    right: Optional[_SoilType] = None
    bottom: Optional[_SoilType] = None
    top: Optional[_SoilType] = None


@dataclass(frozen=True)
class _TileGrouping:
    center: _Tile
    left: _Tile
    right: _Tile
    bottom: _Tile
    top: _Tile

    def matches(self, soil_grouping: _SoilGrouping) -> bool:
        return (
            soil_grouping.center in (None, self.center.soil_type)
            and soil_grouping.left in (None, self.left.soil_type)
            and soil_grouping.right in (None, self.right.soil_type)
            and soil_grouping.bottom in (None, self.bottom.soil_type)
            and soil_grouping.top in (None, self.top.soil_type)
        )


class _Soil:
    def __init__(self, clay_positions: set[Vector2D]) -> None:
        self._bounding_box = BoundingBox.from_points(clay_positions)
        self._tiles = {position: _SoilType.CLAY for position in clay_positions}

    def soil_type(self, position: Vector2D) -> _SoilType:
        return self._tiles.get(position, _SoilType.SAND)

    def set_type(self, position: Vector2D, soil: _SoilType) -> None:
        if soil == _SoilType.SAND:
            self._tiles.pop(position, None)
        else:
            self._tiles[position] = soil

    def adjacent_tile(self, position: Vector2D, direction: CardinalDirection) -> _Tile:
        adjacent_position = position.move(direction, y_grows_down=True)
        return _Tile(adjacent_position, self.soil_type(adjacent_position))

    def tile_grouping(self, position: Vector2D) -> _TileGrouping:
        return _TileGrouping(
            center=_Tile(position, self.soil_type(position)),
            left=self.adjacent_tile(position, CardinalDirection.WEST),
            right=self.adjacent_tile(position, CardinalDirection.EAST),
            bottom=self.adjacent_tile(position, CardinalDirection.SOUTH),
            top=self.adjacent_tile(position, CardinalDirection.NORTH),
        )

    @property
    def num_wet_tiles(self) -> int:
        return sum(
            1
            for tile in self._tiles.values()
            if tile not in (_SoilType.CLAY, _SoilType.SAND)
        )

    @property
    def min_y(self) -> int:
        return self._bounding_box.min_y

    @property
    def max_y(self) -> int:
        return self._bounding_box.max_y

    def __str__(self) -> str:
        min_x, max_x = self._bounding_box.min_x, self._bounding_box.max_x
        min_y, max_y = self._bounding_box.min_y, self._bounding_box.max_y

        def tile_to_str(x: int, y: int) -> str:
            tile = self.soil_type(Vector2D(x, y))
            if tile in (
                _SoilType.BOTTOM_CONFINED_WATER,
                _SoilType.RIGHT_CONFINED_WATER,
                _SoilType.LEFT_CONFINED_WATER,
            ):
                return "|"
            return tile

        return "\n".join(
            [
                "".join([tile_to_str(x, y) for x in range(min_x, max_x + 1)])
                for y in range(min_y, max_y + 1)
            ]
        )


class WaterSpring:
    def __init__(
        self, spring_position: Vector2D, clay_positions: set[Vector2D]
    ) -> None:
        self._spring_position = spring_position
        self._soil = _Soil(clay_positions)

    @property
    def num_wet_tiles(self) -> int:
        return self._soil.num_wet_tiles

    def flow(self) -> None:
        first_wet_position = Vector2D(
            self._spring_position.x,
            max(self._soil.min_y, self._spring_position.y),
        )
        self._propagate_water(first_wet_position)

    def _propagate_water(self, initial_position: Vector2D) -> None:
        positions_to_visit = [initial_position]
        while positions_to_visit:
            position = positions_to_visit.pop(0)
            if position.y > self._soil.max_y:
                continue
            tile_grouping = self._soil.tile_grouping(position)
            new_tile_type = self._new_type_of_tile(tile_grouping)
            if new_tile_type:
                self._soil.set_type(position, new_tile_type)
                positions_to_visit.append(position)
            for neighbor in set(self._neighbors_to_visit(tile_grouping)):
                positions_to_visit.append(neighbor)

    def _new_type_of_tile(self, tile_grouping: _TileGrouping) -> Optional[_SoilType]:
        transformation_table = {
            _SoilGrouping(center=_SoilType.SAND): _SoilType.FLOWING_WATER,
            _SoilGrouping(
                center=_SoilType.FLOWING_WATER,
                bottom=_SoilType.CLAY,
            ): _SoilType.BOTTOM_CONFINED_WATER,
            _SoilGrouping(
                center=_SoilType.FLOWING_WATER,
                bottom=_SoilType.STANDING_WATER,
            ): _SoilType.BOTTOM_CONFINED_WATER,
            _SoilGrouping(
                center=_SoilType.BOTTOM_CONFINED_WATER,
                left=_SoilType.CLAY,
            ): _SoilType.LEFT_CONFINED_WATER,
            _SoilGrouping(
                center=_SoilType.BOTTOM_CONFINED_WATER,
                left=_SoilType.LEFT_CONFINED_WATER,
            ): _SoilType.LEFT_CONFINED_WATER,
            _SoilGrouping(
                center=_SoilType.BOTTOM_CONFINED_WATER,
                right=_SoilType.CLAY,
            ): _SoilType.RIGHT_CONFINED_WATER,
            _SoilGrouping(
                center=_SoilType.BOTTOM_CONFINED_WATER,
                right=_SoilType.RIGHT_CONFINED_WATER,
            ): _SoilType.RIGHT_CONFINED_WATER,
            _SoilGrouping(
                center=_SoilType.BOTTOM_CONFINED_WATER,
                left=_SoilType.STANDING_WATER,
            ): _SoilType.STANDING_WATER,
            _SoilGrouping(
                center=_SoilType.BOTTOM_CONFINED_WATER,
                right=_SoilType.STANDING_WATER,
            ): _SoilType.STANDING_WATER,
            _SoilGrouping(
                center=_SoilType.LEFT_CONFINED_WATER,
                right=_SoilType.CLAY,
            ): _SoilType.STANDING_WATER,
            _SoilGrouping(
                center=_SoilType.LEFT_CONFINED_WATER,
                right=_SoilType.STANDING_WATER,
            ): _SoilType.STANDING_WATER,
            _SoilGrouping(
                center=_SoilType.LEFT_CONFINED_WATER,
                right=_SoilType.RIGHT_CONFINED_WATER,
            ): _SoilType.STANDING_WATER,
            _SoilGrouping(
                center=_SoilType.RIGHT_CONFINED_WATER,
                left=_SoilType.CLAY,
            ): _SoilType.STANDING_WATER,
            _SoilGrouping(
                center=_SoilType.RIGHT_CONFINED_WATER,
                left=_SoilType.STANDING_WATER,
            ): _SoilType.STANDING_WATER,
            _SoilGrouping(
                center=_SoilType.RIGHT_CONFINED_WATER,
                left=_SoilType.LEFT_CONFINED_WATER,
            ): _SoilType.STANDING_WATER,
        }
        for soil_grouping, new_soil_type in transformation_table.items():
            if tile_grouping.matches(soil_grouping):
                return new_soil_type
        return None

    def _neighbors_to_visit(self, tile_grouping: _TileGrouping) -> Iterator[Vector2D]:
        visitation_table = {
            _SoilGrouping(
                center=_SoilType.FLOWING_WATER,
                bottom=_SoilType.SAND,
            ): tile_grouping.bottom.position,
            _SoilGrouping(
                center=_SoilType.BOTTOM_CONFINED_WATER,
                left=_SoilType.SAND,
            ): tile_grouping.left.position,
            _SoilGrouping(
                center=_SoilType.BOTTOM_CONFINED_WATER,
                right=_SoilType.SAND,
            ): tile_grouping.right.position,
            _SoilGrouping(
                center=_SoilType.LEFT_CONFINED_WATER,
                right=_SoilType.SAND,
            ): tile_grouping.right.position,
            _SoilGrouping(
                center=_SoilType.LEFT_CONFINED_WATER,
                right=_SoilType.BOTTOM_CONFINED_WATER,
            ): tile_grouping.right.position,
            _SoilGrouping(
                center=_SoilType.RIGHT_CONFINED_WATER,
                left=_SoilType.SAND,
            ): tile_grouping.left.position,
            _SoilGrouping(
                center=_SoilType.RIGHT_CONFINED_WATER,
                left=_SoilType.BOTTOM_CONFINED_WATER,
            ): tile_grouping.left.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                top=_SoilType.FLOWING_WATER,
            ): tile_grouping.top.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                left=_SoilType.SAND,
            ): tile_grouping.left.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                left=_SoilType.FLOWING_WATER,
            ): tile_grouping.left.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                left=_SoilType.BOTTOM_CONFINED_WATER,
            ): tile_grouping.left.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                left=_SoilType.LEFT_CONFINED_WATER,
            ): tile_grouping.left.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                left=_SoilType.RIGHT_CONFINED_WATER,
            ): tile_grouping.left.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                right=_SoilType.SAND,
            ): tile_grouping.right.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                right=_SoilType.FLOWING_WATER,
            ): tile_grouping.right.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                right=_SoilType.BOTTOM_CONFINED_WATER,
            ): tile_grouping.right.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                right=_SoilType.LEFT_CONFINED_WATER,
            ): tile_grouping.right.position,
            _SoilGrouping(
                center=_SoilType.STANDING_WATER,
                right=_SoilType.RIGHT_CONFINED_WATER,
            ): tile_grouping.right.position,
        }

        for soil_grouping, position in visitation_table.items():
            if tile_grouping.matches(soil_grouping):
                yield position

    def __str__(self) -> str:
        return str(self._soil)
