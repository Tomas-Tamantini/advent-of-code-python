from models.common.io import InputFromString
from ..parser import parse_plant_automaton


def test_parse_plant_automaton():
    file_content = """initial state: #..#.#..##......###...###

                      ...## => #
                      ..#.. => #
                      .#... => #
                      .#.#. => #
                      .#.## => #
                      .##.. => #
                      .#### => #
                      #.#.# => #
                      #.### => #
                      ##.#. => #
                      ##.## => #
                      ###.. => #
                      ###.# => #
                      ####. => #"""
    automaton = parse_plant_automaton(InputFromString(file_content))
    assert automaton.plants_alive(0) == {0, 3, 5, 8, 9, 16, 17, 18, 22, 23, 24}
    assert automaton.plants_alive(20) == {
        -2,
        3,
        4,
        9,
        10,
        11,
        12,
        13,
        17,
        18,
        19,
        20,
        21,
        22,
        23,
        28,
        30,
        33,
        34,
    }
