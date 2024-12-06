from models.common.io import InputFromString

from ..parser import parse_rpg_boss
from ..rpg_game import Fighter


def test_parse_rpg_boss():
    file_content = """Hit Points: 109
                      Damage: 8
                      Armor: 2"""
    boss_kwargs = parse_rpg_boss(InputFromString(file_content))
    boss = Fighter(**boss_kwargs)
    assert boss.hit_points == 109
    assert boss.damage == 8
    assert boss.armor == 2
