from dataclasses import dataclass
from typing import Protocol
from models.common.vectors import Vector2D, CardinalDirection, TurnDirection


@dataclass(frozen=True)
class Ship:
    position: Vector2D = Vector2D(0, 0)
    facing: CardinalDirection = CardinalDirection.EAST
    waypoint: Vector2D = Vector2D(10, 1)


class NavigationInstruction(Protocol):
    def execute(self, ship: Ship) -> Ship: ...


@dataclass(frozen=True)
class MoveShipInstruction:
    direction: CardinalDirection
    distance: int

    def execute(self, ship: Ship) -> Ship:
        return Ship(
            position=ship.position.move(self.direction, self.distance),
            facing=ship.facing,
        )


@dataclass(frozen=True)
class MoveShipForwardInstruction:
    distance: int

    def execute(self, ship: Ship) -> Ship:
        return Ship(
            position=ship.position.move(ship.facing, self.distance), facing=ship.facing
        )


@dataclass(frozen=True)
class TurnShipInstruction:
    turn_direction: TurnDirection

    def execute(self, ship: Ship) -> Ship:
        return Ship(
            position=ship.position, facing=ship.facing.turn(self.turn_direction)
        )


@dataclass(frozen=True)
class MoveWaypointInstruction:
    direction: CardinalDirection
    distance: int

    def execute(self, ship: Ship) -> Ship:
        return Ship(
            position=ship.position,
            facing=ship.facing,
            waypoint=ship.waypoint.move(self.direction, self.distance),
        )


@dataclass(frozen=True)
class MoveTowardsWaypointInstruction:
    times: int

    def execute(self, ship: Ship) -> Ship:
        return Ship(
            position=ship.waypoint * self.times + ship.position,
            facing=ship.facing,
            waypoint=ship.waypoint,
        )


@dataclass(frozen=True)
class RotateWaypointInstruction:
    turn_direction: TurnDirection

    def execute(self, ship: Ship) -> Ship:
        x, y = ship.waypoint.x, ship.waypoint.y
        if self.turn_direction == TurnDirection.RIGHT:
            x, y = y, -x
        elif self.turn_direction == TurnDirection.LEFT:
            x, y = -y, x
        elif self.turn_direction == TurnDirection.U_TURN:
            x, y = -x, -y
        return Ship(
            position=ship.position,
            facing=ship.facing,
            waypoint=Vector2D(x, y),
        )
