from models.common.vectors import Vector2D, CardinalDirection
from ..logic import CubeNet


def test_cube_net_checks_whether_it_contains_given_face():
    net = CubeNet(face_planar_positions={Vector2D(1, 1)})
    assert Vector2D(1, 1) in net
    assert Vector2D(1, 2) not in net


def test_cube_net_iterates_over_faces():
    net = CubeNet(face_planar_positions={Vector2D(1, 1), Vector2D(2, 2)})
    assert set(net) == {Vector2D(1, 1), Vector2D(2, 2)}


def test_cube_net_iterates_over_adjacent_directions_to_given_face():
    net = CubeNet(
        face_planar_positions={Vector2D(1, 1), Vector2D(1, 2), Vector2D(0, 1)}
    )
    assert set(net.directions_with_adjacent_faces(Vector2D(1, 1))) == {
        CardinalDirection.SOUTH,
        CardinalDirection.WEST,
    }
