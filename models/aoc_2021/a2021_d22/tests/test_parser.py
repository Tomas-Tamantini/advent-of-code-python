from models.common.io import InputFromString
from models.common.vectors import Vector3D
from ..parser import parse_cuboid_instructions
from ..reactor_cells import Cuboid, CuboidInstruction


def test_parse_cuboid_instructions():
    file_content = """
                   on x=-48..-3,y=-18..36,z=-26..28
                   off x=-22..-11,y=-42..-27,z=-29..-14"""
    instructions = list(parse_cuboid_instructions(InputFromString(file_content)))
    assert instructions == [
        CuboidInstruction(
            cuboid=Cuboid(
                range_start=Vector3D(-48, -18, -26),
                range_end=Vector3D(-3, 36, 28),
            ),
            is_turn_on=True,
        ),
        CuboidInstruction(
            cuboid=Cuboid(
                range_start=Vector3D(-22, -42, -29),
                range_end=Vector3D(-11, -27, -14),
            ),
            is_turn_on=False,
        ),
    ]
