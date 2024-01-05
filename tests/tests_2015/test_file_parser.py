from typing import Iterator
from input_output.file_parser import FileParser
from models.aoc_2015 import LightGridRegion


class MockFileReader:
    def __init__(self, file_content: str) -> None:
        self._content = file_content

    def read(self, file_name: str) -> str:
        return self._content

    def readlines(self, file_name: str) -> Iterator[str]:
        yield from self._content.split("\n")


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
    FileParser.parse_and_give_light_grid_instruction(instruction, mock_grid)
    instruction = "turn off 820,516 through 871,914"
    FileParser.parse_and_give_light_grid_instruction(instruction, mock_grid)
    instruction = "toggle 427,423 through 929,502"
    FileParser.parse_and_give_light_grid_instruction(instruction, mock_grid)
    assert mock_grid.turn_on_args == LightGridRegion((489, 959), (759, 964))
    assert mock_grid.turn_off_args == LightGridRegion((820, 516), (871, 914))
    assert mock_grid.toggle_args == LightGridRegion((427, 423), (929, 502))


def test_can_parse_and_give_light_grid_instructions_in_elvish_tongue():
    mock_grid_on_off = MockLightGrid()
    instruction = "turn on 489,959 through 759,964"
    FileParser.parse_and_give_light_grid_instruction(
        instruction, mock_grid_on_off, use_elvish_tongue=True
    )
    instruction = "turn off 820,516 through 871,914"
    FileParser.parse_and_give_light_grid_instruction(
        instruction, mock_grid_on_off, use_elvish_tongue=True
    )
    mock_grid_toggle = MockLightGrid()
    instruction = "toggle 427,423 through 929,502"
    FileParser.parse_and_give_light_grid_instruction(
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
    file_reader = MockFileReader(circuit_str)
    file_parser = FileParser(file_reader)
    circuit = file_parser.parse_logic_gates_circuit("some_file_name")
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


def test_can_parse_adirected_graph():
    graph_str = """a to b = 100
                   a to c = 100
                   b to c = 150"""
    file_reader = MockFileReader(graph_str)
    file_parser = FileParser(file_reader)
    graph = file_parser.parse_adirected_graph("some_file_name")
    assert graph.shortest_complete_itinerary_distance() == 200


def test_can_parse_directed_graph():
    graph_str = """Alice would gain 54 happiness units by sitting next to Bob.
                   Bob would lose 7 happiness units by sitting next to Carol.
                   Carol would lose 62 happiness units by sitting next to Alice."""
    file_reader = MockFileReader(graph_str)
    file_parser = FileParser(file_reader)
    graph = file_parser.parse_directed_graph("some_file_name")
    assert graph.round_trip_itinerary_min_cost() == -15
    assert graph.round_trip_itinerary_max_cost() == float("inf")


def test_can_parse_reindeer():
    reindeer_str = (
        "Dancer can fly 27 km/s for 5 seconds, but then must rest for 132 seconds."
    )
    reindeer = FileParser.parse_reindeer(reindeer_str)
    assert reindeer.flight_speed == 27
    assert reindeer.flight_interval == 5
    assert reindeer.rest_interval == 132


def test_can_parse_cookie_properties():
    properties_str = (
        "PeanutButter: capacity -1, durability 3, flavor 0, texture 2, calories 1"
    )
    ingredient_properties = FileParser.parse_cookie_properties(properties_str)
    assert ingredient_properties.capacity == -1
    assert ingredient_properties.durability == 3
    assert ingredient_properties.flavor == 0
    assert ingredient_properties.texture == 2
    assert ingredient_properties.calories == 1


def test_can_parse_rpg_boss():
    file_content = """Hit Points: 109
                      Damage: 8
                      Armor: 2"""
    file_reader = MockFileReader(file_content)
    file_parser = FileParser(file_reader)
    boss = file_parser.parse_rpg_boss("some_file_name")
    assert boss.hit_points == 109
    assert boss.damage == 8
    assert boss.armor == 2
