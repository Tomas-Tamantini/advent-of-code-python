from ..logic import SpriteScreen


def test_sprite_screen_draws_one_pixel_per_cycle_checking_if_sprite_occupies_that_pixel():
    sprite_center_positions = [1, 1, 16, 16, 5, 5]
    expected = "##..##"
    screen = SpriteScreen(width=6, height=1, sprite_length=3)
    message = screen.draw(sprite_center_positions)
    assert message == expected
