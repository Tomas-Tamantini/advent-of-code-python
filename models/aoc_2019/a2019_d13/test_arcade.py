from .arcade import (
    ArcadeGameScreen,
    ArcadeGameTile,
    ArcadeGameInput,
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


def test_can_set_and_reset_current_score_on_arcade_game():
    screen = ArcadeGameScreen()
    assert screen.current_score == 0
    screen.reset_score(123)
    assert screen.current_score == 123
    screen.reset_score(321)
    assert screen.current_score == 321


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


def test_arcade_game_output_of_minus_and_zero_sets_current_score():
    screen = ArcadeGameScreen()
    output = ArcadeGameOutput(screen)
    for out in (-1, 0, 123):
        output.write(out)
    assert screen.current_score == 123


def test_can_run_arcade_game_and_query_screen():
    instructions = [104, 1, 104, 2, 104, 3, 104, 6, 104, 5, 104, 4, 99]
    screen = ArcadeGameScreen()
    run_intcode_arcade(instructions, screen)
    assert screen.get_tile(1, 2) == ArcadeGameTile.PADDLE
    assert screen.get_tile(6, 5) == ArcadeGameTile.BALL


def test_can_query_ball_and_paddle_positions():
    screen = ArcadeGameScreen()
    screen.draw_tile(0, 1, ArcadeGameTile.BALL)
    screen.draw_tile(10, 11, ArcadeGameTile.PADDLE)
    assert screen.ball_x == 0
    assert screen.paddle_x == 10


def test_arcade_game_input_returns_zero_if_paddle_and_ball_are_aligned():
    screen = ArcadeGameScreen()
    screen.draw_tile(0, 1, ArcadeGameTile.BALL)
    screen.draw_tile(0, 11, ArcadeGameTile.PADDLE)
    arcade_input = ArcadeGameInput(screen)
    assert arcade_input.read() == 0


def test_arcade_game_input_returns_minus_one_if_ball_is_to_the_left_of_paddle():
    screen = ArcadeGameScreen()
    screen.draw_tile(0, 1, ArcadeGameTile.BALL)
    screen.draw_tile(10, 11, ArcadeGameTile.PADDLE)
    arcade_input = ArcadeGameInput(screen)
    assert arcade_input.read() == -1


def test_arcade_game_input_returns_one_if_ball_is_to_the_right_of_paddle():
    screen = ArcadeGameScreen()
    screen.draw_tile(12, 1, ArcadeGameTile.BALL)
    screen.draw_tile(10, 11, ArcadeGameTile.PADDLE)
    arcade_input = ArcadeGameInput(screen)
    screen.draw_tile(0, 11, ArcadeGameTile.PADDLE)
    assert arcade_input.read() == 1
