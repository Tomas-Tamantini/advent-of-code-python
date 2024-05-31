from ..programmable_screen import ProgrammableScreen


def test_can_light_up_rectangle_of_pixels():
    screen = ProgrammableScreen(7, 3)
    screen.rect(3, 2)
    assert screen.number_of_lit_pixels() == 6


def test_can_rotate_row_left():
    screen = ProgrammableScreen(7, 3)
    screen.rect(3, 2)
    screen.rotate_row(row=1, offset=2)
    screen.rect(3, 2)
    assert screen.number_of_lit_pixels() == 8


def test_can_rotate_column_down():
    screen = ProgrammableScreen(7, 3)
    screen.rect(3, 2)
    screen.rotate_column(column=1, offset=1)
    screen.rect(3, 2)
    assert screen.number_of_lit_pixels() == 7


def test_rotation_wraps_around():
    screen = ProgrammableScreen(7, 3)
    screen.rect(3, 2)
    screen.rotate_row(row=1, offset=1000)
    assert screen.number_of_lit_pixels() == 6


def test_screen_has_str_representation():
    screen = ProgrammableScreen(7, 3)
    screen.rect(3, 2)
    screen.rotate_column(column=1, offset=1)
    screen.rotate_row(row=0, offset=4)
    screen.rotate_column(column=1, offset=1)
    assert str(screen) == "0100101\n1010000\n0100000"
