from models.aoc_2017 import PackageRouter


def test_maze_without_letters_yields_no_letters():
    router = PackageRouter(
        maze=[
            " | ",
            " | ",
        ]
    )
    router.explore()
    assert router.visited_letters == []


def test_maze_is_explored_starting_from_first_row():
    router = PackageRouter(
        maze=[
            " | ",
            " A ",
            " | ",
            " B ",
        ]
    )
    router.explore()
    assert router.visited_letters == ["A", "B"]


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
    router.explore()
    assert router.visited_letters == ["A", "B", "C", "D", "E", "F"]


def test_can_keep_track_of_number_of_steps_in_package_routing():
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
    router.explore()
    assert router.num_steps == 38
