from models.common.vectors import Vector2D
from ..logic import BlizzardNavigator


def test_blizzard_navigator_can_move_in_all_four_directions_or_stay_put():
    navigator = BlizzardNavigator(position=Vector2D(15, 25), time=3)
    neighbors = list(navigator.next_states())
    assert len(neighbors) == 5
    assert set(neighbors) == {
        BlizzardNavigator(position=Vector2D(15, 24), time=4),
        BlizzardNavigator(position=Vector2D(15, 26), time=4),
        BlizzardNavigator(position=Vector2D(14, 25), time=4),
        BlizzardNavigator(position=Vector2D(16, 25), time=4),
        BlizzardNavigator(position=Vector2D(15, 25), time=4),
    }
