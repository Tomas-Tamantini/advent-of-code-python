from .logic import TunnelMaze
from models.common.io import InputReader, CharacterGrid
from models.common.vectors import Vector2D


def _tunnel_updated_characters(
    grid: CharacterGrid, split_entrance_four_ways: bool
) -> dict[Vector2D, chr]:
    if not split_entrance_four_ways:
        return dict()
    entrance_position = next(grid.positions_with_value("@"))
    updated_chars = dict()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            offset = Vector2D(dx, dy)
            new_char = "@" if offset.manhattan_size == 2 else "#"
            updated_chars[entrance_position + offset] = new_char
    return updated_chars


def parse_tunnel_maze(
    input_reader: InputReader, split_entrance_four_ways: bool = False
) -> TunnelMaze:
    content = input_reader.read()
    grid = CharacterGrid(content)
    maze = TunnelMaze()
    updated_chars = _tunnel_updated_characters(grid, split_entrance_four_ways)
    for position in grid.positions():
        original_char = grid.tiles[position]
        actual_char = updated_chars.get(position, original_char)
        if actual_char == ".":
            maze.add_open_passage(position)
        if actual_char == "@":
            maze.add_entrance(position)
        if actual_char.islower():
            maze.add_key(position, key_id=original_char)
        if actual_char.isupper():
            maze.add_door(position, corresponding_key_id=actual_char.lower())
    return maze
