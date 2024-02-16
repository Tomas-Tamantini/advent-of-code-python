from typing import Iterator


class CelestialBody:
    def __init__(self, name: str) -> None:
        self._name = name
        self._satellites = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def satellites(self) -> Iterator["CelestialBody"]:
        return self._satellites

    def add_satellite(self, satellite: "CelestialBody") -> None:
        self._satellites.append(satellite)

    def count_orbits(self, depth: int = 0) -> int:
        return depth + sum(
            satellite.count_orbits(depth + 1) for satellite in self.satellites
        )
