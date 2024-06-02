from dataclasses import dataclass
from models.common.vectors import Vector2D
from .cave_map import CaveMap
from .cave_game import CaveGame
from .units import CaveGameUnit
from .game_state import CaveGameState


@dataclass(frozen=True)
class CaveTeamSpec:
    attack_power: int
    hit_points: int


def _build_unit(unit_id: str, position: Vector2D, specs: CaveTeamSpec) -> CaveGameUnit:
    return CaveGameUnit(
        unit_id=unit_id,
        hit_points=specs.hit_points,
        attack_power=specs.attack_power,
        position=position,
    )


def build_cave_game(
    map_with_units: str,
    elf_specs: CaveTeamSpec = CaveTeamSpec(3, 200),
    goblin_specs: CaveTeamSpec = CaveTeamSpec(3, 200),
) -> CaveGame:
    elves = []
    goblins = []
    for y, line in enumerate(map_with_units.split("\n")):
        for x, char in enumerate(line.strip()):
            if char == "E":
                elves.append(
                    _build_unit(
                        unit_id=f"E{len(elves)+1}",
                        position=Vector2D(x, y),
                        specs=elf_specs,
                    )
                )
            elif char == "G":
                goblins.append(
                    _build_unit(
                        unit_id=f"G{len(goblins)+1}",
                        position=Vector2D(x, y),
                        specs=goblin_specs,
                    )
                )
    cave_map = CaveMap(map_with_units.replace("E", ".").replace("G", "."))
    initial_state = CaveGameState(elves=tuple(elves), goblins=tuple(goblins))
    return CaveGame(cave_map, initial_state)
