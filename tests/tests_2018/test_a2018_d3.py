from models.aoc_2018 import FabricRectangle, FabricArea


def test_non_overlapping_rectangles_return_empty_intersection():
    rectangle_a = FabricRectangle(
        id=0, inches_from_left=1, inches_from_top=3, width=4, height=4
    )
    rectangle_b = FabricRectangle(
        id=1, inches_from_left=5, inches_from_top=5, width=2, height=2
    )
    assert set(rectangle_a.intersection(rectangle_b)) == set()


def test_overlapping_rectangles_return_intersection_points():
    rectangle_a = FabricRectangle(
        id=0, inches_from_left=1, inches_from_top=3, width=4, height=4
    )
    rectangle_b = FabricRectangle(
        id=1, inches_from_left=3, inches_from_top=1, width=4, height=4
    )
    assert set(rectangle_a.intersection(rectangle_b)) == {
        (3, 3),
        (3, 4),
        (4, 3),
        (4, 4),
    }


def test_can_find_points_claimed_by_more_than_one_rectangle():
    rectangles = [
        FabricRectangle(id=0, inches_from_left=1, inches_from_top=3, width=4, height=4),
        FabricRectangle(id=1, inches_from_left=3, inches_from_top=1, width=4, height=4),
        FabricRectangle(id=2, inches_from_left=5, inches_from_top=5, width=2, height=2),
        FabricRectangle(id=3, inches_from_left=6, inches_from_top=6, width=2, height=2),
    ]
    area = FabricArea()
    area.distribute(rectangles)
    assert area.points_with_more_than_one_claim == {
        (3, 3),
        (3, 4),
        (4, 3),
        (4, 4),
        (6, 6),
    }
