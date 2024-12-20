from collections import defaultdict

from models.common.io import CharacterGrid

from ..logic import CpuRacetrack

_RACETRACK = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############"""


def _example_racetrack() -> CpuRacetrack:
    grid = CharacterGrid(_RACETRACK)
    start = next(grid.positions_with_value("S"))
    end = next(grid.positions_with_value("E"))
    return CpuRacetrack(
        start,
        end,
        track_positions=set(grid.positions_with_value(".")) | {start, end},
        wall_positions=set(grid.positions_with_value("#")),
    )


def test_cpu_racetrack_yields_advantageous_cheats():
    track = _example_racetrack()
    cheat_count = defaultdict(int)
    for cheat in track.advantageous_cheats():
        cheat_count[cheat.saved_time] += 1
    assert cheat_count == {
        2: 14,
        4: 14,
        6: 2,
        8: 4,
        10: 2,
        12: 3,
        20: 1,
        36: 1,
        38: 1,
        40: 1,
        64: 1,
    }
