from .scaffold_map import ScaffoldMap
from .path_compression import CompressedPath


class CameraOutput:
    def __init__(self, scaffold_map: ScaffoldMap) -> None:
        self._scaffold_map = scaffold_map

    def write(self, value: int) -> None:
        self._scaffold_map.add_pixel(chr(value))


class VacuumRobotOutput:
    def __init__(self) -> None:
        self._output_value = -1

    def write(self, value: int) -> None:
        self._output_value = value

    @property
    def output_value(self) -> int:
        return self._output_value


class VacuumRobotInput:
    def __init__(
        self, compressed_path: CompressedPath, watch_video_feed: bool = False
    ) -> None:
        main_routine = compressed_path.main_routine
        subroutines = list(compressed_path.subroutines_in_order())
        watch = "y" if watch_video_feed else "n"
        self._input_stream = (
            main_routine + "\n" + "\n".join(subroutines) + "\n" + watch + "\n"
        )
        self._current_position = 0

    def read(self) -> int:
        value = ord(self._input_stream[self._current_position])
        self._current_position += 1
        return value
