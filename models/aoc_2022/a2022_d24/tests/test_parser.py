from models.common.io import InputFromString
from models.common.vectors import Vector2D

from ..parser import parse_blizzard_valley


def test_parse_blizzard_valley():
    valley = """
             #.#####
             #>...<#
             #^..v.#
             #####.#
             """
    result = parse_blizzard_valley(InputFromString(valley))
    assert result.entrance == Vector2D(1, 0)
    assert result.exit == Vector2D(5, 3)
    assert result.is_wall(Vector2D(6, 3))
    assert not result.position_is_free_at_time(Vector2D(1, 1), 0)
    assert not result.position_is_free_at_time(Vector2D(1, 1), 1)
    assert result.position_is_free_at_time(Vector2D(1, 1), 2)
