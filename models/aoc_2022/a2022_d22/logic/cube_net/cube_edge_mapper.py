from collections import defaultdict
from dataclasses import dataclass

from models.common.vectors import CardinalDirection, Vector2D, Vector3D

from .cube_navigator import CubeNavigator
from .cube_net import CubeNet


@dataclass(frozen=True)
class _Edge:
    face_planar_position: Vector2D
    side: CardinalDirection


@dataclass(frozen=True)
class _FaceGeometry:
    face_planar_position: Vector2D
    top_left: Vector3D
    x_hat: Vector3D
    y_hat: Vector3D

    @property
    def bottom_left(self) -> Vector3D:
        return self.top_left + self.y_hat

    @property
    def bottom_right(self) -> Vector3D:
        return self.top_left + self.x_hat + self.y_hat

    @property
    def top_right(self) -> Vector3D:
        return self.top_left + self.x_hat

    @property
    def normal(self) -> Vector3D:
        return self.y_hat.vector_product(self.x_hat)

    def vertices(self, side: CardinalDirection) -> tuple[Vector3D, Vector3D]:
        if side == CardinalDirection.NORTH:
            return self.top_left, self.top_right
        elif side == CardinalDirection.SOUTH:
            return self.bottom_left, self.bottom_right
        elif side == CardinalDirection.WEST:
            return self.top_left, self.bottom_left
        else:
            return self.top_right, self.bottom_right

    def neighbor(self, side: CardinalDirection) -> "_FaceGeometry":
        neighbor = self.face_planar_position.move(side, y_grows_down=True)
        if side == CardinalDirection.SOUTH:
            return _FaceGeometry(
                neighbor,
                top_left=self.top_left + self.y_hat,
                x_hat=self.x_hat,
                y_hat=self.normal,
            )
        elif side == CardinalDirection.NORTH:
            return _FaceGeometry(
                neighbor,
                top_left=self.top_left + self.normal,
                x_hat=self.x_hat,
                y_hat=-self.normal,
            )
        elif side == CardinalDirection.EAST:
            return _FaceGeometry(
                neighbor,
                top_left=self.top_left + self.x_hat,
                x_hat=self.normal,
                y_hat=self.y_hat,
            )
        else:
            return _FaceGeometry(
                neighbor,
                top_left=self.top_left + self.normal,
                x_hat=-self.normal,
                y_hat=self.y_hat,
            )


class CubeEdgeMapper:
    def __init__(self, cube_net: CubeNet) -> None:
        self._cube_net = cube_net
        self._edge_correspondence = self._build_edge_correspondence()

    def _build_edge_correspondence(self) -> dict[_Edge, _Edge]:
        edges = defaultdict(list)
        for geometry in self._geometries():
            for direction in CardinalDirection:
                edges[frozenset(geometry.vertices(direction))].append(
                    _Edge(geometry.face_planar_position, direction)
                )
        correspondencies = dict()
        for edge_pair in edges.values():
            correspondencies[edge_pair[0]] = edge_pair[1]
            correspondencies[edge_pair[1]] = edge_pair[0]
        return correspondencies

    def _geometries(self) -> set[_FaceGeometry]:
        first_geometry = _FaceGeometry(
            next(iter(self._cube_net)),
            top_left=Vector3D(0, 0, 0),
            x_hat=Vector3D(1, 0, 0),
            y_hat=Vector3D(0, 1, 0),
        )
        face_stack = {first_geometry}
        visited = set()
        while face_stack:
            face = face_stack.pop()
            if face in visited:
                continue
            visited.add(face)
            for direction in self._cube_net.directions_with_adjacent_faces(
                face.face_planar_position
            ):
                neighbor_geometry = face.neighbor(direction)
                face_stack.add(neighbor_geometry)
        return visited

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
