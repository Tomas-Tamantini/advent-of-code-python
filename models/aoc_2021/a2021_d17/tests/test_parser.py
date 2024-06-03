from models.common.io import InputFromString
from models.common.vectors import BoundingBox, Vector2D
from ..parser import parse_bounding_box


def test_parse_bounding_box():
    file_content = "target area: x=244..303, y=-91..-54"
    bounding_box = parse_bounding_box(InputFromString(file_content))
    assert bounding_box == BoundingBox(
        bottom_left=Vector2D(244, -91), top_right=Vector2D(303, -54)
    )
