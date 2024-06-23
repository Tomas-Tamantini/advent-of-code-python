from models.common.io import IOHandler, CharacterGrid
from .game_of_life_lights import GameOfLifeLights


def aoc_2015_d18(io_handler: IOHandler) -> None:
    io_handler.output_writer.write_header(2015, 18, "Like a GIF For Your Yard")
    grid = CharacterGrid(io_handler.input_reader.read())
    initial_cells = set(grid.positions_with_value("#"))
    game = GameOfLifeLights(grid.width, grid.height)
    num_steps = 100
    cells_default_game = initial_cells
    cells_corners_always_on_game = initial_cells
    corner_cells = set(game.corner_cells)
    for _ in range(num_steps):
        cells_default_game = game.next_state(cells_default_game)
        cells_corners_always_on_game = game.step_with_always_on_cells(
            cells_corners_always_on_game, corner_cells
        )
    print(
        f"Part 1: There are {len(cells_default_game)} lights on after {num_steps} steps"
    )
    print(
        f"Part 2: There are {len(cells_corners_always_on_game)} lights on after {num_steps} steps with corner lights always on"
    )
