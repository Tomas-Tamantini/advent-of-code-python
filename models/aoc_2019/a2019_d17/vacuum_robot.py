from dataclasses import dataclass
from models.vectors import Vector2D, TurnDirection, CardinalDirection


@dataclass(frozen=True)
class VacuumRobotInstruction:
    turn: TurnDirection
    steps: int

    def __str__(self) -> str:
        return f"{self.turn.value},{self.steps}"


@dataclass(frozen=True)
class VacuumRobot:
    position: Vector2D
    direction: CardinalDirection

    def new_position(self, instruction: VacuumRobotInstruction) -> Vector2D:
        new_direction = self.direction.turn(instruction.turn)
        new_position = self.position.move(
            new_direction, num_steps=instruction.steps, y_grows_down=True
        )
        return new_position

    def move(self, instruction: VacuumRobotInstruction) -> "VacuumRobot":
        new_direction = self.direction.turn(instruction.turn)
        new_position = self.position.move(
            new_direction, num_steps=instruction.steps, y_grows_down=True
        )
        return VacuumRobot(new_position, new_direction)
