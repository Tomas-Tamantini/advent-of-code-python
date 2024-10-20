from models.common.vectors import Vector2D
from .garden import BoundedGarden, PacmanGarden


def test_gardener_can_step_in_all_four_directions():
    garden = BoundedGarden(width=3, height=3, rock_positions=set())
    neighboring_positions = set(garden.neighboring_positions(Vector2D(1, 1)))
    assert neighboring_positions == {
        Vector2D(1, 0),
        Vector2D(0, 1),
        Vector2D(1, 2),
        Vector2D(2, 1),
    }


def test_gardener_cannot_step_outside_bounded_garden():
    garden = BoundedGarden(width=3, height=3, rock_positions=set())
    neighboring_positions = set(garden.neighboring_positions(Vector2D(0, 0)))
    assert neighboring_positions == {Vector2D(1, 0), Vector2D(0, 1)}


def test_gardener_can_step_outside_pacman_garden():
    garden = PacmanGarden(width=3, height=3, rock_positions=set())
    neighboring_positions = set(garden.neighboring_positions(Vector2D(0, 0)))
    assert neighboring_positions == {
        Vector2D(1, 0),
        Vector2D(0, 1),
        Vector2D(0, -1),
        Vector2D(-1, 0),
    }


def test_gardener_cannot_step_into_rock_cell():
    garden = PacmanGarden(
        width=3, height=3, rock_positions={Vector2D(0, 1), Vector2D(2, 0)}
    )
    neighboring_positions = set(garden.neighboring_positions(Vector2D(0, 0)))
    assert neighboring_positions == {Vector2D(1, 0), Vector2D(0, -1)}


def test_garden_yields_next_positions():
    garden = BoundedGarden(width=5, height=5, rock_positions=set())
    current_positions = {Vector2D(0, 0), Vector2D(4, 4)}
    neighboring_positions = set(garden.next_positions(current_positions))
    assert neighboring_positions == {
        Vector2D(1, 0),
        Vector2D(0, 1),
        Vector2D(3, 4),
        Vector2D(4, 3),
    }
