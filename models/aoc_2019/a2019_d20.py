from models.vectors import Vector2D
from models.graphs import GridMaze


class PortalMaze(GridMaze):
    def __init__(self) -> None:
        super().__init__()
        self._entrance = None
        self._exit = None

    def set_entrance(self, entrance: Vector2D) -> None:
        self._entrance = entrance

    def set_exit(self, exit: Vector2D) -> None:
        self._exit = exit

    def add_portal(self, portal_a: Vector2D, portal_b: Vector2D) -> None:
        self._try_add_edge(portal_a, portal_b, 1)

    def num_steps_to_solve(self) -> int:
        self.reduce(irreducible_nodes={self._entrance, self._exit})
        return self.shortest_distance(self._entrance, self._exit)
