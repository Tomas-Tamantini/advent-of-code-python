from models.common.io import InputFromString

from ..light_grid import LightGridRegion
from ..parser import parse_and_give_light_grid_instructions


class MockLightGrid:
    def __init__(self) -> None:
        self.turn_on_args = None
        self.turn_off_args = None
        self.toggle_args = None
        self.increase_brightness_args = []
        self.decrease_brightness_args = []

    def turn_on(self, region: LightGridRegion) -> None:
        self.turn_on_args = region

    def turn_off(self, region: LightGridRegion) -> None:
        self.turn_off_args = region

    def toggle(self, region: LightGridRegion) -> None:
        self.toggle_args = region

    def increase_brightness(self, region: LightGridRegion, increase: int) -> None:
        self.increase_brightness_args = [region, increase]

    def decrease_brightness(self, region: LightGridRegion, decrease: int) -> None:
        self.decrease_brightness_args = [region, decrease]


def test_parse_and_give_light_grid_instructions():
    mock_grid = MockLightGrid()
    input_reader = InputFromString(
        """
        turn on 489,959 through 759,964
        turn off 820,516 through 871,914
        toggle 427,423 through 929,502
        """
    )
    parse_and_give_light_grid_instructions(input_reader, mock_grid)
    assert mock_grid.turn_on_args == LightGridRegion((489, 959), (759, 964))
    assert mock_grid.turn_off_args == LightGridRegion((820, 516), (871, 914))
    assert mock_grid.toggle_args == LightGridRegion((427, 423), (929, 502))


def test_parse_and_give_light_grid_instructions_in_elvish_tongue():
    mock_grid_on_off = MockLightGrid()
    input_reader = InputFromString(
        """
        turn on 489,959 through 759,964
        turn off 820,516 through 871,914
        """
    )
    parse_and_give_light_grid_instructions(
        input_reader, mock_grid_on_off, use_elvish_tongue=True
    )
    mock_grid_toggle = MockLightGrid()
    input_reader = InputFromString("toggle 427,423 through 929,502")
    parse_and_give_light_grid_instructions(
        input_reader, mock_grid_toggle, use_elvish_tongue=True
    )
    assert mock_grid_on_off.increase_brightness_args == [
        LightGridRegion((489, 959), (759, 964)),
        1,
    ]
    assert mock_grid_on_off.decrease_brightness_args == [
        LightGridRegion((820, 516), (871, 914)),
        1,
    ]
    assert mock_grid_toggle.increase_brightness_args == [
        LightGridRegion((427, 423), (929, 502)),
        2,
    ]
