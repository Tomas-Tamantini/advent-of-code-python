from .solution import houses_with_at_least_one_present


def test_santa_always_delivers_a_present_to_starting_house():
    assert len(houses_with_at_least_one_present("")) == 1


def test_santa_travels_in_two_d_grid_according_to_instructions():
    assert len(houses_with_at_least_one_present("^>v>")) == 5


def test_santa_can_give_more_than_one_present_to_a_house():
    assert len(houses_with_at_least_one_present("^v^v^v^v^v")) == 2
