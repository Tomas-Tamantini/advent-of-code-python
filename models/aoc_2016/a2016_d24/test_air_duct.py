from .air_duct import AirDuctMaze


def test_if_no_points_of_interest_pairwise_distances_are_empty():
    blueprint = ["#####", "#0..#", "#####"]
    maze = AirDuctMaze(blueprint)
    assert maze.pairwise_distances() == dict()


def test_if_single_point_of_interest_pairwise_distances_has_one_element():
    blueprint = [
        "#####",
        "#0..#",
        "#.#1#",
        "#...#",
        "#####",
    ]
    maze = AirDuctMaze(blueprint)
    assert maze.pairwise_distances() == {("0", "1"): 3}


def test_if_multiple_points_of_interest_all_pairwise_shortest_distances_are_returned():
    blueprint = [
        "###########",
        "#0.1.....2#",
        "#.#######.#",
        "#4.......3#",
        "###########",
    ]
    maze = AirDuctMaze(blueprint)
    assert maze.pairwise_distances() == {
        ("0", "1"): 2,
        ("0", "2"): 8,
        ("0", "3"): 10,
        ("0", "4"): 2,
        ("1", "2"): 6,
        ("1", "3"): 8,
        ("1", "4"): 4,
        ("2", "3"): 2,
        ("2", "4"): 10,
        ("3", "4"): 8,
    }


def test_can_find_min_num_steps_to_visit_all_points_of_interest_with_and_without_returning_to_origin():
    blueprint = [
        "###########",
        "#0.1.....2#",
        "#.#######.#",
        "#4.......3#",
        "###########",
    ]
    maze = AirDuctMaze(blueprint)
    assert (
        maze.min_num_steps_to_visit_points_of_interest(must_return_to_origin=False)
        == 14
    )
    assert (
        maze.min_num_steps_to_visit_points_of_interest(must_return_to_origin=True) == 20
    )
