from models.aoc_2019.a2019_d13 import (
    ArcadeGameScreen,
    ArcadeGameTile,
    ArcadeGameOutput,
    run_intcode_arcade,
)


def test_game_screen_default_tile_is_empty():
    screen = ArcadeGameScreen()
    assert screen.get_tile(123, 321) == ArcadeGameTile.EMPTY


def test_can_draw_tile_on_arcade_game():
    screen = ArcadeGameScreen()
    screen.draw_tile(123, 321, ArcadeGameTile.WALL)
    assert screen.get_tile(123, 321) == ArcadeGameTile.WALL


def test_can_draw_over_same_tile_on_arcade_game():
    screen = ArcadeGameScreen()
    screen.draw_tile(123, 321, ArcadeGameTile.WALL)
    screen.draw_tile(123, 321, ArcadeGameTile.PADDLE)
    assert screen.get_tile(123, 321) == ArcadeGameTile.PADDLE


def test_can_count_number_of_given_tile_on_arcade_game():
    screen = ArcadeGameScreen()
    screen.draw_tile(0, 0, ArcadeGameTile.WALL)
    screen.draw_tile(0, 0, ArcadeGameTile.PADDLE)
    screen.draw_tile(10, 10, ArcadeGameTile.BALL)
    screen.draw_tile(10, 10, ArcadeGameTile.BALL)
    screen.draw_tile(100, 100, ArcadeGameTile.PADDLE)
    assert screen.count_tiles(ArcadeGameTile.PADDLE) == 2
    assert screen.count_tiles(ArcadeGameTile.BALL) == 1
    assert screen.count_tiles(ArcadeGameTile.WALL) == 0


def test_arcade_game_output_draws_tile_parsing_every_three_outputs_as_x_y_and_type():
    screen = ArcadeGameScreen()
    output = ArcadeGameOutput(screen)
    for out in (1, 2, 3, 6, 5, 4):
        output.write(out)
    assert screen.get_tile(1, 2) == ArcadeGameTile.PADDLE
    assert screen.get_tile(6, 5) == ArcadeGameTile.BALL


def test_can_run_arcade_game_and_query_screen():
    instructions = [104, 1, 104, 2, 104, 3, 104, 6, 104, 5, 104, 4, 99]
    screen = ArcadeGameScreen()
    run_intcode_arcade(instructions, screen)
    assert screen.get_tile(1, 2) == ArcadeGameTile.PADDLE
    assert screen.get_tile(6, 5) == ArcadeGameTile.BALL
