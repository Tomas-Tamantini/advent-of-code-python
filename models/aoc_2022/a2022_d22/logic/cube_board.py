from models.common.vectors import Vector2D
from .board_navigator import BoardNavigator
from .edge_mapper import EdgeMapper
from .cube_navigator import CubeNavigator


class CubeBoard:
    def __init__(self, edge_mapper: EdgeMapper) -> None:
        self._edge_mapper = edge_mapper

    @property
    def initial_position(self) -> Vector2D:
        return self._edge_mapper.cube_net.topmost_left_position()

    def move_navigator_forward(
        self, navigator: BoardNavigator, num_steps: int
    ) -> BoardNavigator:
        cube_net = self._edge_mapper.cube_net
        cube_navigator = cube_net.board_navigator_to_cube_navigator(navigator)
        for _ in range(num_steps):
            if cube_navigator.is_about_to_leave_cube_face(cube_net.edge_length):
                new_cube_navigator = self._edge_mapper.next_navigator_state(
                    cube_navigator
                )
            else:
                new_cube_navigator = CubeNavigator(
                    cube_face=cube_navigator.cube_face,
                    relative_position=cube_navigator.relative_position.move(
                        cube_navigator.facing, y_grows_down=True
                    ),
                    facing=cube_navigator.facing,
                )
            if new_cube_navigator.hit_wall():
                break
            else:
                cube_navigator = new_cube_navigator

        return cube_net.cube_navigator_to_board_navigator(cube_navigator)
