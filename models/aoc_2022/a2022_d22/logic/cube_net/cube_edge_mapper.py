from dataclasses import dataclass
from models.common.vectors import Vector2D, Vector3D, CardinalDirection
from .cube_net import CubeNet
from .cube_navigator import CubeNavigator
from collections import defaultdict


@dataclass(frozen=True)
class _Edge:
    face_planar_position: Vector2D
    side: CardinalDirection


@dataclass(frozen=True)
class _FaceGeometry:
    face_planar_position: Vector2D
    bottom_left: Vector3D
    x_hat: Vector3D
    y_hat: Vector3D

    @property
    def top_left(self) -> Vector3D:
        return self.bottom_left + self.y_hat

    @property
    def top_right(self) -> Vector3D:
        return self.bottom_left + self.x_hat + self.y_hat

    @property
    def bottom_right(self) -> Vector3D:
        return self.bottom_left + self.x_hat

    @property
    def normal(self) -> Vector3D:
        return self.x_hat.vector_product(self.y_hat)


class CubeEdgeMapper:
    def __init__(self, cube_net: CubeNet) -> None:
        self._edge_correspondence = self._build_edge_correspondence(cube_net)

    @staticmethod
    def _build_edge_correspondence(cube_net: CubeNet) -> dict[_Edge, _Edge]:
        # TODO: Refactor
        face_stack = {
            _FaceGeometry(
                next(iter(cube_net)),
                bottom_left=Vector3D(0, 0, 0),
                x_hat=Vector3D(1, 0, 0),
                y_hat=Vector3D(0, 1, 0),
            )
        }
        visited = set()
        while face_stack:
            face = face_stack.pop()
            if face in visited:
                continue
            visited.add(face)
            for direction in CardinalDirection:
                neighbor = face.face_planar_position.move(direction, y_grows_down=True)
                if neighbor in cube_net:
                    if direction == CardinalDirection.SOUTH:
                        neighbor_geometry = _FaceGeometry(
                            neighbor,
                            bottom_left=face.bottom_left + face.y_hat,
                            x_hat=face.x_hat,
                            y_hat=face.normal,
                        )
                    elif direction == CardinalDirection.NORTH:
                        neighbor_geometry = _FaceGeometry(
                            neighbor,
                            bottom_left=face.bottom_left + face.normal,
                            x_hat=face.x_hat,
                            y_hat=-face.normal,
                        )
                    elif direction == CardinalDirection.EAST:
                        neighbor_geometry = _FaceGeometry(
                            neighbor,
                            bottom_left=face.bottom_left + face.x_hat,
                            x_hat=face.normal,
                            y_hat=face.y_hat,
                        )
                    else:
                        neighbor_geometry = _FaceGeometry(
                            neighbor,
                            bottom_left=face.bottom_left + face.normal,
                            x_hat=-face.normal,
                            y_hat=face.y_hat,
                        )
                    face_stack.add(neighbor_geometry)
        edges = defaultdict(list)
        for geometry in visited:
            edges[frozenset({geometry.bottom_left, geometry.top_left})].append(
                _Edge(geometry.face_planar_position, CardinalDirection.WEST)
            )
            edges[frozenset({geometry.top_left, geometry.top_right})].append(
                _Edge(geometry.face_planar_position, CardinalDirection.SOUTH)
            )
            edges[frozenset({geometry.top_right, geometry.bottom_right})].append(
                _Edge(geometry.face_planar_position, CardinalDirection.EAST)
            )
            edges[frozenset({geometry.bottom_right, geometry.bottom_left})].append(
                _Edge(geometry.face_planar_position, CardinalDirection.NORTH)
            )
        correspondencies = dict()
        for edge_pair in edges.values():
            correspondencies[edge_pair[0]] = edge_pair[1]
            correspondencies[edge_pair[1]] = edge_pair[0]
        return correspondencies

    def next_navigator(self, navigator: CubeNavigator) -> CubeNavigator:
        current_edge = _Edge(
            face_planar_position=navigator.face_planar_position,
            side=navigator.facing,
        )
        new_edge = self._edge_correspondence[current_edge]
        return CubeNavigator(
            face_planar_position=new_edge.face_planar_position,
            facing=new_edge.side.reverse(),
        )
