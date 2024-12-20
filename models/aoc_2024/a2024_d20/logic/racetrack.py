from models.common.vectors import Vector2D


class CpuRacetrack:
    def __init__(
        self,
        start: Vector2D,
        end: Vector2D,
        track_positions: set[Vector2D],
        wall_positions: set[Vector2D],
    ):
        self._start = start
        self._end = end
        self._track_positions = track_positions
        self._wall_positions = wall_positions
