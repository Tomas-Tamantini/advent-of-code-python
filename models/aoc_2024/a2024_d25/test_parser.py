from models.common.io import InputFromString

from .parser import parse_keys, parse_locks

_FILE_CONTENT = """#####
                   .####
                   .####
                   .####
                   .#.#.
                   .#...
                   .....

                   #####
                   ##.##
                   .#.##
                   ...##
                   ...#.
                   ...#.
                   .....

                   .....
                   #....
                   #....
                   #...#
                   #.#.#
                   #.###
                   #####

                   .....
                   .....
                   #.#..
                   ###..
                   ###.#
                   ###.#
                   #####

                   .....
                   .....
                   .....
                   #....
                   #.#..
                   #.#.#
                   #####"""


def test_parse_locks():
    input_reader = InputFromString(_FILE_CONTENT)
    locks = list(parse_locks(input_reader))
    assert locks == [(0, 5, 3, 4, 3), (1, 2, 0, 5, 3)]


def test_parse_keys():
    input_reader = InputFromString(_FILE_CONTENT)
    keys = list(parse_keys(input_reader))
    assert keys == [(5, 0, 2, 1, 3), (4, 3, 4, 0, 2), (3, 0, 2, 0, 1)]
