from typing import Iterator


class CelestialBody:
    def __init__(self, name: str) -> None:
        self._name = name
        self._parent = None
        self._satellites = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def satellites(self) -> Iterator["CelestialBody"]:
        return self._satellites

    def add_satellite(self, satellite: "CelestialBody") -> None:
        self._satellites.append(satellite)
        satellite._parent = self

    def count_orbits(self, depth: int = 0) -> int:
        return depth + sum(
            satellite.count_orbits(depth + 1) for satellite in self.satellites
        )

    def _path_to(self, name: str) -> list[str]:
        if self.name == name:
            return [self.name]
        for satellite in self.satellites:
            path = satellite._path_to(name)
            if path:
                return [self.name] + path
        return []

    def orbital_distance(self, start: str, end: str) -> int:
        path_to_start = self._path_to(start)
        path_to_end = self._path_to(end)
        ancestor_index = 0
        while (
            ancestor_index < len(path_to_start)
            and ancestor_index < len(path_to_end)
            and path_to_start[ancestor_index] == path_to_end[ancestor_index]
        ):
            ancestor_index += 1
        return len(path_to_start) + len(path_to_end) - 2 * (ancestor_index)
