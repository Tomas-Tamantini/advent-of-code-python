from models.common.vectors import Vector3D

from ..logic import Brick, BricksDag


def test_bricks_dag_keeps_track_of_which_bricks_would_fall_if_given_one_was_removed():
    bricks = [
        Brick(start=Vector3D(0, 0, 1), end=Vector3D(0, 0, 5)),
        Brick(start=Vector3D(-5, 0, 6), end=Vector3D(5, 0, 6)),
        Brick(start=Vector3D(-5, 0, 7), end=Vector3D(-5, 3, 7)),
        Brick(start=Vector3D(5, 0, 7), end=Vector3D(5, 3, 7)),
        Brick(start=Vector3D(-5, 3, 8), end=Vector3D(5, 3, 8)),
        Brick(start=Vector3D(5, 3, 9), end=Vector3D(5, 3, 9)),
    ]
    dag = BricksDag(set(bricks))
    assert set(dag.bricks_that_would_topple(bricks[0])) == {*bricks[1:]}
    assert set(dag.bricks_that_would_topple(bricks[1])) == {*bricks[2:]}
    assert set(dag.bricks_that_would_topple(bricks[2])) == set()
    assert set(dag.bricks_that_would_topple(bricks[3])) == set()
    assert set(dag.bricks_that_would_topple(bricks[4])) == {bricks[5]}
    assert set(dag.bricks_that_would_topple(bricks[5])) == set()
