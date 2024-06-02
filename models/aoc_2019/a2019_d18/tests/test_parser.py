from models.common.io import InputFromString
from ..parser import parse_tunnel_maze


def test_parse_tunnel_maze():
    file_content = """
                   a.C
                   .@.
                   ..b
                   """
    maze = parse_tunnel_maze(InputFromString(file_content))
    assert maze.shortest_distance_to_all_keys() == 6


def test_tunnel_maze_can_have_entrance_split_in_four():
    file_content = """
                   a...c
                   .....
                   ..@..
                   .....
                   b...d
                   """
    maze = parse_tunnel_maze(
        InputFromString(file_content), split_entrance_four_ways=True
    )
    assert maze.shortest_distance_to_all_keys() == 8
