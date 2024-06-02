from models.common.io import InputFromString
from ..parser import parse_fabric_rectangles
from ..fabric_area import FabricRectangle


def test_parse_fabric_rectangles():
    file_content = """#1 @ 1,3: 2x4
                      #213 @ 34,17: 13x29"""
    rectangles = list(parse_fabric_rectangles(InputFromString(file_content)))
    assert rectangles == [
        FabricRectangle(id=1, inches_from_left=1, inches_from_top=3, width=2, height=4),
        FabricRectangle(
            id=213, inches_from_left=34, inches_from_top=17, width=13, height=29
        ),
    ]
