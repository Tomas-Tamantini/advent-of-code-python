from input_output.file_parser import (
    parse_and_give_light_grid_instruction,
    parse_logic_gates_circuit,
    LightGridRegion,
)


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


def test_can_parse_and_give_light_grid_instructions():
    mock_grid = MockLightGrid()
    instruction = "turn on 489,959 through 759,964"
    parse_and_give_light_grid_instruction(instruction, mock_grid)
    instruction = "turn off 820,516 through 871,914"
    parse_and_give_light_grid_instruction(instruction, mock_grid)
    instruction = "toggle 427,423 through 929,502"
    parse_and_give_light_grid_instruction(instruction, mock_grid)
    assert mock_grid.turn_on_args == LightGridRegion((489, 959), (759, 964))
    assert mock_grid.turn_off_args == LightGridRegion((820, 516), (871, 914))
    assert mock_grid.toggle_args == LightGridRegion((427, 423), (929, 502))


def test_can_parse_and_give_light_grid_instructions_in_elvish_tongue():
    mock_grid_on_off = MockLightGrid()
    instruction = "turn on 489,959 through 759,964"
    parse_and_give_light_grid_instruction(
        instruction, mock_grid_on_off, use_elvish_tongue=True
    )
    instruction = "turn off 820,516 through 871,914"
    parse_and_give_light_grid_instruction(
        instruction, mock_grid_on_off, use_elvish_tongue=True
    )
    mock_grid_toggle = MockLightGrid()
    instruction = "toggle 427,423 through 929,502"
    parse_and_give_light_grid_instruction(
        instruction, mock_grid_toggle, use_elvish_tongue=True
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


def test_can_parse_logic_gates_circuit():
    circuit_str = """123 -> x
                     456 -> y
                     x AND y -> d
                     x OR y -> e
                     x LSHIFT 2 -> f
                     y RSHIFT 2 -> g
                     NOT x -> h
                     NOT y -> i"""

    circuit = parse_logic_gates_circuit(circuit_str)
    expected_values = {
        "x": 123,
        "y": 456,
        "d": 72,
        "e": 507,
        "f": 492,
        "g": 114,
        "h": 65412,
        "i": 65079,
    }
    for wire, value in expected_values.items():
        assert circuit.get_value(wire) == value