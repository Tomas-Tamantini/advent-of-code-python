from models.common.io import InputFromString
from ..parser import parse_celestial_bodies


def test_parse_celestial_bodies():
    file_content = """COM)A
                      B)C
                      COM)B"""
    com = parse_celestial_bodies(InputFromString(file_content))
    assert com.name == "COM"
    com_children = list(com.satellites)
    assert com_children[0].name == "A"
    assert len(list(com_children[0].satellites)) == 0
    assert com_children[1].name == "B"
    b_children = list(com_children[1].satellites)
    assert b_children[0].name == "C"
