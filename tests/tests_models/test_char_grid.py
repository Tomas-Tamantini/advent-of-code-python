from models.common.io import CharacterGrid
from models.common.vectors import Vector2D

text = """
       abc
       def
       """


def test_character_grid_extracts_width_and_height_from_text_ignoring_empty_spaces():
    grid = CharacterGrid(text)
    assert grid.width == 3
    assert grid.height == 2


def test_character_grid_builds_dictionary_of_tile_position_and_tile_char():
    assert CharacterGrid(text).tiles == {
        Vector2D(0, 0): "a",
        Vector2D(1, 0): "b",
        Vector2D(2, 0): "c",
        Vector2D(0, 1): "d",
        Vector2D(1, 1): "e",
        Vector2D(2, 1): "f",
    }


def test_character_grid_iterates_through_all_positions():
    assert set(CharacterGrid(text).positions()) == {
        Vector2D(0, 0),
        Vector2D(1, 0),
        Vector2D(2, 0),
        Vector2D(0, 1),
        Vector2D(1, 1),
        Vector2D(2, 1),
    }


def test_character_grid_returns_position_of_center_tile():
    text = """
           abcde
           fghij
           klmno
           """
    assert CharacterGrid(text).center == Vector2D(2, 1)


def test_character_grid_yields_all_positions_with_given_value():
    text = """
           .#.
           ##.
           """
    expected = {Vector2D(1, 0), Vector2D(0, 1), Vector2D(1, 1)}
    assert set(CharacterGrid(text).positions_with_value("#")) == expected
