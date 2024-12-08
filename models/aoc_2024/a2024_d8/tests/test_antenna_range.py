from models.common.vectors import Vector2D

from ..logic import Antenna, AntennaRange, TwiceDistanceAntinodeGenerator


def _example_range_a() -> AntennaRange:
    return AntennaRange(
        width=10,
        height=10,
        antennas={
            Antenna(frequency="a", position=Vector2D(x=4, y=3)),
            Antenna(frequency="a", position=Vector2D(x=8, y=4)),
            Antenna(frequency="a", position=Vector2D(x=5, y=5)),
            Antenna(frequency="A", position=Vector2D(x=6, y=7)),
        },
    )


def _example_range_b() -> AntennaRange:
    return AntennaRange(
        width=12,
        height=12,
        antennas={
            Antenna(frequency="0", position=Vector2D(x=4, y=4)),
            Antenna(frequency="0", position=Vector2D(x=5, y=2)),
            Antenna(frequency="0", position=Vector2D(x=7, y=3)),
            Antenna(frequency="0", position=Vector2D(x=8, y=1)),
            Antenna(frequency="A", position=Vector2D(x=6, y=5)),
            Antenna(frequency="A", position=Vector2D(x=8, y=8)),
            Antenna(frequency="A", position=Vector2D(x=9, y=9)),
        },
    )


def test_antenna_range_lists_all_antinodes_within_bounds():
    antenna_range = _example_range_a()
    antinodes = set(antenna_range.antinodes(TwiceDistanceAntinodeGenerator()))
    assert antinodes == {
        Vector2D(3, 1),
        Vector2D(0, 2),
        Vector2D(2, 6),
        Vector2D(6, 7),
    }

    assert (
        len(set(_example_range_b().antinodes(TwiceDistanceAntinodeGenerator()))) == 14
    )
