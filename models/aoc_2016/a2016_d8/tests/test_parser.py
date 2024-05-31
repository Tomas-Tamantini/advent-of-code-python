from unittest.mock import Mock
from models.common.io import InputFromString
from ..parser import parse_programmable_screen_instructions
from ..programmable_screen import ProgrammableScreen


def test_parse_programmable_screen_instructions():
    file_content = """rect 3x2
                      rotate column x=1 by 1
                      rotate row y=0 by 4"""
    screen_spy = Mock(ProgrammableScreen)
    parse_programmable_screen_instructions(InputFromString(file_content), screen_spy)
    assert screen_spy.rect.call_args_list == [((3, 2),)]
    assert screen_spy.rotate_column.call_args_list == [((1, 1),)]
    assert screen_spy.rotate_row.call_args_list == [((0, 4),)]
