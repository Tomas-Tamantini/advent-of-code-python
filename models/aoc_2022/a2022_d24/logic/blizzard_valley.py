from models.common.vectors import Vector2D
from .blizzard import Blizzard


class BlizzardValley:
    def __init__(
        self,
        height: int,
        width: int,
        entrance: Vector2D,
        exit: Vector2D,
        blizzards: set[Blizzard],
    ):
        self._height = height
        self._width = width
        self._entrance = entrance
        self._exit = exit
        self._blizzards = blizzards

    @property
    def entrance(self) -> Vector2D:
        return self._entrance

    @property
    def exit(self) -> Vector2D:
        return self._exit

    def _is_border(self, position: Vector2D) -> bool:
        return (
            position.x <= 0
            or position.x >= self._width - 1
            or position.y <= 0
            or position.y >= self._height - 1
        )

    def _blizzard_position(self, blizzard: Blizzard, time: int) -> Vector2D:
        position = blizzard.initial_position.move(
            blizzard.direction, num_steps=time, y_grows_down=True
        )
        x = (position.x - 1) % (self._width - 2) + 1
        y = (position.y - 1) % (self._height - 2) + 1
        return Vector2D(x, y)

    def is_wall(self, position: Vector2D) -> bool:
        return (
            self._is_border(position)
            and position != self._entrance
            and position != self._exit
        )

    def _position_occupied_by_blizzard(self, position: Vector2D, time: int) -> bool:
        return any(
            self._blizzard_position(blizzard, time) == position
            for blizzard in self._blizzards
        )

    def position_is_free_at_time(self, position: Vector2D, time: int) -> bool:
        return not self.is_wall(position) and not self._position_occupied_by_blizzard(
            position, time
        )
