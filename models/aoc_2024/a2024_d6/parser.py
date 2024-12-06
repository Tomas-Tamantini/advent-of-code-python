from models.common.io import CharacterGrid
from models.common.vectors import CardinalDirection
from .logic import PatrolGuard, PatrolArea


def parse_patrol_area(character_grid: CharacterGrid) -> PatrolArea:
    return PatrolArea(
        character_grid.width,
        character_grid.height,
        set(character_grid.positions_with_value("#")),
    )


def parse_patrol_guard(character_grid: CharacterGrid) -> PatrolGuard:
    guard_position = next(character_grid.positions_with_value("^"))
    return PatrolGuard(guard_position, CardinalDirection.NORTH)
