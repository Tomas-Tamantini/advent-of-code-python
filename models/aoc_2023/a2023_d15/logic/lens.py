from dataclasses import dataclass


@dataclass(frozen=True)
class Lens:
    label: str
    focal_strength: int
