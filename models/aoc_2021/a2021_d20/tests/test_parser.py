from models.common.io import InputFromString
from models.common.vectors import Vector2D

from ..parser import parse_trench_rules_and_trench_map


def test_parse_trench_rules_and_trench_map():
    file_content = """..#.#......#..#

                      #..#.
                      #....
                      """
    trench_rule, trench_map = parse_trench_rules_and_trench_map(
        InputFromString(file_content)
    )
    assert trench_rule == {2, 4, 11, 14}
    assert trench_map == {Vector2D(0, 0), Vector2D(3, 0), Vector2D(0, 1)}
