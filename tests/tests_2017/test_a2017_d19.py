from models.aoc_2017 import PackageRouter


def test_maze_without_letters_yields_no_letters():
    router = PackageRouter(
        maze=[
            " | ",
            " | ",
        ]
    )
    assert list(router.visited_letters()) == []


def test_maze_is_explored_starting_from_first_row():
    router = PackageRouter(
        maze=[
            " | ",
            " A ",
            " | ",
            " B ",
        ]
    )
    assert list(router.visited_letters()) == ["A", "B"]


def test_maze_can_make_turns():
    router = PackageRouter(
        maze=[
            "     |          ",
            "     |  +--+    ",
            "     A  |  C    ",
            " F---|----E|--+ ",
            "     |  |  |  D ",
            "     +B-+  +--+ ",
        ]
    )
    assert list(router.visited_letters()) == ["A", "B", "C", "D", "E", "F"]
