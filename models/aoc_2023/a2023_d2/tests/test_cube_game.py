from ..logic import CubeAmount, CubeGame


def test_bag_is_possible_if_all_colors_are_geq_to_colors_of_all_handfuls():
    game = CubeGame(
        game_id=1,
        handfuls=[
            CubeAmount({"red": 1, "green": 2}),
            CubeAmount({"blue": 10, "red": 3}),
        ],
    )
    bag = CubeAmount({"red": 4, "green": 2, "blue": 10})
    assert game.bag_amount_is_possible(bag)


def test_bag_is_not_possible_if_some_color_is_lt_color_of_some_handful():
    game = CubeGame(
        game_id=1,
        handfuls=[
            CubeAmount({"red": 1, "green": 2}),
            CubeAmount({"blue": 10, "red": 3}),
        ],
    )
    bag = CubeAmount({"red": 2, "green": 2, "blue": 10})
    assert not game.bag_amount_is_possible(bag)


def test_minimum_bag_is_merge_of_all_handfuls():
    game = CubeGame(
        game_id=1,
        handfuls=[
            CubeAmount({"red": 1, "green": 2}),
            CubeAmount({"blue": 10, "red": 3}),
        ],
    )
    assert game.minimum_bag() == CubeAmount({"red": 3, "green": 2, "blue": 10})
