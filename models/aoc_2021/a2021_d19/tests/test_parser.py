from models.common.io import InputFromString
from models.common.vectors import Vector3D
from ..parser import parse_underwater_scanners
from ..underwater_scanner import UnderwaterScanner


def test_parse_underwater_scanners():
    file_content = """
                   --- scanner 0 ---
                   0,2,1
                   4,1,2
                   3,3,3

                   --- scanner 1 ---
                   -1,-1,-1
                   -5,0, -2
                   -2,1, -3
                   """
    scanners = list(parse_underwater_scanners(InputFromString(file_content)))
    assert scanners == [
        UnderwaterScanner(
            scanner_id=0,
            visible_beacons_relative_coordinates=(
                Vector3D(0, 2, 1),
                Vector3D(4, 1, 2),
                Vector3D(3, 3, 3),
            ),
        ),
        UnderwaterScanner(
            scanner_id=1,
            visible_beacons_relative_coordinates=(
                Vector3D(-1, -1, -1),
                Vector3D(-5, 0, -2),
                Vector3D(-2, 1, -3),
            ),
        ),
    ]
