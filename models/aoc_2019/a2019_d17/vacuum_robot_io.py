from .scaffold_map import ScaffoldMap


class CameraOutput:
    def __init__(self, scaffold_map: ScaffoldMap) -> None:
        self._scaffold_map = scaffold_map

    def write(self, value: int) -> None:
        self._scaffold_map.add_pixel(chr(value))
