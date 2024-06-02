from models.common.io import InputFromString
from ..parser import parse_multi_technique_shuffle


def test_parse_shuffle_techniques():
    file_content = """
                   deal into new stack
                   cut -2
                   deal with increment 7
                   cut 8
                   cut -4
                   deal with increment 7
                   cut 3
                   deal with increment 9
                   deal with increment 3
                   cut -1
                   """
    shuffle = parse_multi_technique_shuffle(InputFromString(file_content))
    assert shuffle.new_card_position(position_before_shuffle=3, deck_size=10) == 8
