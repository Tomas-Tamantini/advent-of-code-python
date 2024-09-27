import pytest
from models.common.vectors import (
    CardinalDirection,
    Vector2D,
    TurnDirection,
    BoundingBox,
    Vector3D,
    VectorNDimensional,
    HexagonalDirection,
    CanonicalHexagonalCoordinates,
    Orientation,
    twice_polygon_area,
    num_grid_points_inside_polygon,
)


def test_can_get_manhattan_distance_for_vector_2d():
    assert Vector2D(1, 2).manhattan_distance(Vector2D(4, -3)) == 8


def test_can_get_manhattan_size_for_vector_2d():
    assert Vector2D(1, -2).manhattan_size == 3


def test_vectors_can_be_added_together():
    assert Vector2D(1, 2) + Vector2D(3, 4) == Vector2D(4, 6)


def test_vectors_can_be_subtracted_from_each_other():
    assert Vector2D(1, 2) - Vector2D(3, 4) == Vector2D(-2, -2)


def test_vectors_can_be_multiplied_by_a_scalar():
    assert Vector2D(1, 2) * 3 == 3 * Vector2D(1, 2) == Vector2D(3, 6)


def test_vector_product_of_two_d_vectors_yields_int():
    assert Vector2D(1, 2).vector_product_2d(Vector2D(3, 4)) == -2


def test_dot_product_of_two_vectors_yields_int():
    assert Vector2D(1, 2).dot_product(Vector2D(3, 4)) == 11


def test_vector_moves_by_one_step_by_default():
    assert Vector2D(0, 0).move(CardinalDirection.NORTH) == Vector2D(0, 1)
    assert Vector2D(0, 0).move(CardinalDirection.EAST) == Vector2D(1, 0)
    assert Vector2D(0, 0).move(CardinalDirection.SOUTH) == Vector2D(0, -1)
    assert Vector2D(0, 0).move(CardinalDirection.WEST) == Vector2D(-1, 0)


def test_vector_can_move_specified_number_of_steps():
    assert Vector2D(10, 10).move(CardinalDirection.NORTH, 5) == Vector2D(10, 15)


def test_vector_can_specify_direction_of_y_axis():
    assert Vector2D(10, 10).move(
        CardinalDirection.NORTH, y_grows_down=True
    ) == Vector2D(10, 9)
    assert Vector2D(10, 10).move(
        CardinalDirection.SOUTH, y_grows_down=True
    ) == Vector2D(10, 11)


def test_vector_has_two_adjacent_positions_not_including_diagonal_by_default():
    assert set(Vector2D(0, 0).adjacent_positions()) == {
        Vector2D(0, 1),
        Vector2D(1, 0),
        Vector2D(0, -1),
        Vector2D(-1, 0),
    }


def test_vector_has_eight_adjacent_positions_including_diagonal():
    assert set(Vector2D(0, 0).adjacent_positions(include_diagonals=True)) == {
        Vector2D(0, 1),
        Vector2D(1, 0),
        Vector2D(0, -1),
        Vector2D(-1, 0),
        Vector2D(1, 1),
        Vector2D(1, -1),
        Vector2D(-1, -1),
        Vector2D(-1, 1),
    }


def test_cardinal_directions_are_vertical_or_horizontal():
    assert CardinalDirection.NORTH.is_vertical
    assert CardinalDirection.SOUTH.is_vertical
    assert not CardinalDirection.EAST.is_vertical
    assert not CardinalDirection.WEST.is_vertical

    assert CardinalDirection.EAST.is_horizontal
    assert CardinalDirection.WEST.is_horizontal
    assert not CardinalDirection.NORTH.is_horizontal
    assert not CardinalDirection.SOUTH.is_horizontal


def test_cardinal_directions_can_be_spun_around():
    assert CardinalDirection.NORTH.turn_left() == CardinalDirection.WEST
    assert CardinalDirection.WEST.turn_left() == CardinalDirection.SOUTH
    assert CardinalDirection.SOUTH.turn_left() == CardinalDirection.EAST
    assert CardinalDirection.EAST.turn_left() == CardinalDirection.NORTH

    assert CardinalDirection.NORTH.turn_right() == CardinalDirection.EAST
    assert CardinalDirection.EAST.turn_right() == CardinalDirection.SOUTH
    assert CardinalDirection.SOUTH.turn_right() == CardinalDirection.WEST
    assert CardinalDirection.WEST.turn_right() == CardinalDirection.NORTH

    assert CardinalDirection.NORTH.reverse() == CardinalDirection.SOUTH
    assert CardinalDirection.EAST.reverse() == CardinalDirection.WEST
    assert CardinalDirection.SOUTH.reverse() == CardinalDirection.NORTH
    assert CardinalDirection.WEST.reverse() == CardinalDirection.EAST

    assert (
        CardinalDirection.NORTH.turn(TurnDirection.NO_TURN) == CardinalDirection.NORTH
    )
    assert CardinalDirection.WEST.turn(TurnDirection.LEFT) == CardinalDirection.SOUTH
    assert CardinalDirection.SOUTH.turn(TurnDirection.RIGHT) == CardinalDirection.WEST
    assert CardinalDirection.EAST.turn(TurnDirection.U_TURN) == CardinalDirection.WEST


def test_bottom_left_cannot_be_to_the_right_of_top_right():
    with pytest.raises(ValueError):
        BoundingBox(Vector2D(2, 0), Vector2D(1, 0))


def test_bottom_left_cannot_be_to_the_top_of_top_right():
    with pytest.raises(ValueError):
        BoundingBox(Vector2D(0, 2), Vector2D(0, 1))


def test_bounding_box_with_bottom_left_equal_to_top_right_has_all_dimensions_zero():
    bounding_box = BoundingBox(Vector2D(1, 2), Vector2D(1, 2))
    assert bounding_box.width == bounding_box.height == bounding_box.area == 0


def test_bounding_box_has_min_and_max_x_and_y_properties():
    bounding_box = BoundingBox(Vector2D(1, 2), Vector2D(4, 6))
    assert bounding_box.min_x == 1
    assert bounding_box.max_x == 4
    assert bounding_box.min_y == 2
    assert bounding_box.max_y == 6


def test_bounding_box_has_top_left_and_bottom_right_properties():
    bounding_box = BoundingBox(bottom_left=Vector2D(1, 2), top_right=Vector2D(4, 6))
    assert bounding_box.top_left == Vector2D(1, 6)
    assert bounding_box.bottom_right == Vector2D(4, 2)


def test_bounding_box_dimensions_are_calculated_properly():
    bounding_box = BoundingBox(Vector2D(1, 2), Vector2D(4, 6))
    assert bounding_box.width == 3
    assert bounding_box.height == 4
    assert bounding_box.area == 12


def test_bounding_box_of_zero_points_has_all_dimensions_zero():
    bounding_box = BoundingBox.from_points([])
    assert bounding_box.width == bounding_box.height == bounding_box.area == 0


def test_can_iterate_through_all_points_in_bounding_box():
    bounding_box = BoundingBox(bottom_left=Vector2D(1, 2), top_right=Vector2D(3, 5))
    assert set(bounding_box.all_points_contained()) == {
        Vector2D(1, 2),
        Vector2D(2, 2),
        Vector2D(3, 2),
        Vector2D(1, 3),
        Vector2D(2, 3),
        Vector2D(3, 3),
        Vector2D(1, 4),
        Vector2D(2, 4),
        Vector2D(3, 4),
        Vector2D(1, 5),
        Vector2D(2, 5),
        Vector2D(3, 5),
    }


def test_can_check_whether_bounding_box_contains_a_point():
    bounding_box = BoundingBox(Vector2D(1, 2), Vector2D(4, 6))
    assert bounding_box.contains(Vector2D(1, 2))
    assert bounding_box.contains(Vector2D(4, 6))
    assert bounding_box.contains(Vector2D(2, 3))
    assert not bounding_box.contains(Vector2D(0, 2))
    assert not bounding_box.contains(Vector2D(1, 1))
    assert not bounding_box.contains(Vector2D(4, 7))


def test_bounding_box_of_multiple_points_is_smallest_possible():
    points = [
        Vector2D(100, 1000),
        Vector2D(200, 2000),
        Vector2D(200, 1000),
        Vector2D(150, 1500),
    ]
    bounding_box = BoundingBox.from_points(points)
    assert bounding_box == BoundingBox(Vector2D(100, 1000), Vector2D(200, 2000))


def test_intersection_of_two_bounding_boxes_which_do_not_intersect_is_empty():
    box_a = BoundingBox(bottom_left=Vector2D(0, 0), top_right=Vector2D(10, 20))
    box_b = BoundingBox(bottom_left=Vector2D(11, 21), top_right=Vector2D(30, 40))
    assert box_a.intersection(box_b) is None


def test_intersection_of_two_overlapping_bounding_boxes_is_their_common_area():
    box_a = BoundingBox(bottom_left=Vector2D(0, 0), top_right=Vector2D(10, 20))
    box_b = BoundingBox(bottom_left=Vector2D(5, 10), top_right=Vector2D(15, 18))
    assert box_a.intersection(box_b) == BoundingBox(
        bottom_left=Vector2D(5, 10), top_right=Vector2D(10, 18)
    )


def test_can_iterate_through_vector_3d_coordinates():
    vector = Vector3D(x=1, y=2, z=3)
    assert list(vector) == [1, 2, 3]


def test_can_access_vector_3d_coordinates_by_index_and_name():
    vector = Vector3D(x=1, y=2, z=3)
    assert vector.x == vector[0] == 1
    assert vector.y == vector[1] == 2
    assert vector.z == vector[2] == 3


def test_can_get_manhattan_distance_for_vector_3d():
    assert Vector3D(1, 2, 3).manhattan_distance(Vector3D(4, -3, 2)) == 9


def test_can_get_manhattan_size_for_vector_3d():
    assert Vector3D(1, -2, 3).manhattan_size == 6


def test_can_add_vectors_3d_together():
    assert Vector3D(1, 2, 3) + Vector3D(4, 5, 6) == Vector3D(5, 7, 9)


def test_can_subtract_vectors_3d_from_each_other():
    assert Vector3D(1, 2, 3) - Vector3D(3, 2, 1) == Vector3D(-2, 0, 2)


def test_3d_vector_can_be_negated():
    assert -Vector3D(1, 2, 3) == Vector3D(-1, -2, -3)


def test_3d_vector_can_be_multiplied_by_a_scalar():
    assert Vector3D(1, 2, 3) * 3 == 3 * Vector3D(1, 2, 3) == Vector3D(3, 6, 9)


def test_3d_vector_has_26_adjacent_positions_if_diagonal_steps_are_permitted():
    assert len(list(Vector3D(0, 0, 0).adjacent_positions(include_diagonals=True))) == 26


def test_3d_vector_has_6_adjacent_positions_if_diagonal_steps_are_not_permitted():
    assert len(list(Vector3D(0, 0, 0).adjacent_positions(include_diagonals=False))) == 6


def test_vector_product_of_3d_vectors_is_anti_commutative():
    vec_a = Vector3D(1, 2, 3)
    vec_b = Vector3D(4, 5, 6)
    assert vec_a.vector_product(vec_b) == Vector3D(-3, 6, -3)
    assert vec_b.vector_product(vec_a) == Vector3D(3, -6, 3)


def test_3d_vectors_can_be_sorted_lexicographically():
    assert sorted(
        [
            Vector3D(1, 2, 3),
            Vector3D(2, 1, 3),
            Vector3D(1, 2, 4),
            Vector3D(1, 3, 3),
        ]
    ) == [
        Vector3D(1, 2, 3),
        Vector3D(1, 2, 4),
        Vector3D(1, 3, 3),
        Vector3D(2, 1, 3),
    ]


def test_n_dimensional_vector_can_be_compared_for_equality():
    assert VectorNDimensional(1, 2, 3) == VectorNDimensional(1, 2, 3)
    assert VectorNDimensional(1, 2, 3) != VectorNDimensional(1, 2, 4)
    assert VectorNDimensional(1, 2, 3) != VectorNDimensional(1, 2, 3, 4)
    assert hash(VectorNDimensional(1, 2, 3)) == hash(VectorNDimensional(1, 2, 3))


def test_can_add_two_n_dimensional_vectors():
    a = VectorNDimensional(1, 2, 3, 4)
    b = VectorNDimensional(5, 6, 7, 8)
    assert a + b == VectorNDimensional(6, 8, 10, 12)


def test_4d_vector_has_80_adjacent_positions():
    assert len(list(VectorNDimensional(1, 2, 3, 4).adjacent_positions())) == 80


def test_hexagonal_coordinates_are_hashable_and_equality_comparable():
    pos1 = CanonicalHexagonalCoordinates(1, 2)
    pos2 = CanonicalHexagonalCoordinates(1, 2)
    pos3 = CanonicalHexagonalCoordinates(2, 1)
    assert pos1 == pos2
    assert hash(pos1) == hash(pos2)
    assert pos1 != pos3
    assert hash(pos1) != hash(pos3)


def test_shortest_number_of_steps_in_hexagonal_coordinates_is_sum_of_coordinates_if_both_have_same_sign():
    assert CanonicalHexagonalCoordinates(1, 2).num_steps_away_from_origin() == 3
    assert CanonicalHexagonalCoordinates(-123, -321).num_steps_away_from_origin() == 444


def test_shortest_number_of_steps_in_hexagonal_coordinates_is_max_of_coordinates_if_they_have_opposite_signs():
    assert CanonicalHexagonalCoordinates(1, -2).num_steps_away_from_origin() == 2
    assert CanonicalHexagonalCoordinates(-123, 321).num_steps_away_from_origin() == 321


def test_can_move_along_hexagonal_coordinates():
    pos = CanonicalHexagonalCoordinates(num_steps_north=3, num_steps_northeast=7)
    pos = pos.move(direction=HexagonalDirection.NORTH, num_steps=-2)
    assert pos == CanonicalHexagonalCoordinates(1, 7)
    pos = pos.move(direction=HexagonalDirection.SOUTH, num_steps=-3)
    assert pos == CanonicalHexagonalCoordinates(4, 7)
    pos = pos.move(direction=HexagonalDirection.NORTHEAST, num_steps=1)
    assert pos == CanonicalHexagonalCoordinates(4, 8)
    pos = pos.move(direction=HexagonalDirection.SOUTHWEST, num_steps=3)
    assert pos == CanonicalHexagonalCoordinates(4, 5)
    pos = pos.move(direction=HexagonalDirection.NORTHWEST, num_steps=2)
    assert pos == CanonicalHexagonalCoordinates(6, 3)
    pos = pos.move(direction=HexagonalDirection.SOUTHEAST, num_steps=-1)
    assert pos == CanonicalHexagonalCoordinates(7, 2)


def test_hexagonal_coordinate_has_six_adjacent_positions():
    assert set(CanonicalHexagonalCoordinates(0, 0).adjacent_positions()) == {
        CanonicalHexagonalCoordinates(0, 1),
        CanonicalHexagonalCoordinates(1, 0),
        CanonicalHexagonalCoordinates(0, -1),
        CanonicalHexagonalCoordinates(-1, 0),
        CanonicalHexagonalCoordinates(1, -1),
        CanonicalHexagonalCoordinates(-1, 1),
    }


def test_orientation_z_axis_is_vector_product_of_x_and_y_axis():
    orientation = Orientation(
        x_prime=Vector3D(0, 1, 0),
        y_prime=Vector3D(0, 0, -1),
    )
    assert orientation.z_prime == Vector3D(-1, 0, 0)


def test_there_are_24_orientations_aligned_with_grid_axes():
    orientations = Orientation.all_orientations_aligned_with_grid_axes()
    assert len(list(orientations)) == 24


def test_coordinates_in_given_orientation_can_be_reverted_to_absolute_coordinates():
    orientation = Orientation(
        x_prime=Vector3D(0, 1, 0),
        y_prime=Vector3D(0, 0, -1),
    )
    absolute_coordinates = orientation.to_absolute_coordinates(Vector3D(1, 2, 3))
    assert absolute_coordinates == Vector3D(-3, 1, -2)


@pytest.mark.parametrize(
    "vertices, twice_area",
    [
        ([], 0),
        ([(0, 0)], 0),
        ([(0, 0), (1, 0)], 0),
        ([(0, 0), (1, 0), (0, 1)], 1),
        ([(1, 6), (3, 1), (7, 2), (4, 4), (8, 5)], 33),
    ],
)
def test_twice_area_of_polygon_is_calculated_with_shoelace_theorem(
    vertices, twice_area
):
    vertices_as_vectors = [Vector2D(*vertex) for vertex in vertices]
    assert twice_polygon_area(vertices_as_vectors) == twice_area


@pytest.mark.parametrize(
    "vertices, num_grid_points",
    [
        ([], 0),
        ([(0, 0)], 0),
        ([(0, 0), (1, 0)], 0),
        ([(0, 0), (1, 0), (0, 1)], 0),
        ([(1, 6), (3, 1), (7, 2), (4, 4), (8, 5)], 15),
        ([(1, 0), (4, 3), (4, 5), (0, 3)], 7),
    ],
)
def test_number_of_grid_points_inside_polygon_calculated_with_picks_theorem(
    vertices, num_grid_points
):
    vertices_as_vectors = [Vector2D(*vertex) for vertex in vertices]
    assert num_grid_points_inside_polygon(vertices_as_vectors) == num_grid_points
