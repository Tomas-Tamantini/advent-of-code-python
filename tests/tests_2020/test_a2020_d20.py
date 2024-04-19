import pytest
from random import shuffle, seed
from typing import Hashable
from models.vectors import Vector2D, CardinalDirection
from models.aoc_2020.a2020_d20 import (
    JigsawPieceOrientation,
    solve_jigsaw,
    JigsawPiece,
    JigsawPieceBinaryImage,
    SolvedJigsaw,
)


def test_there_are_eight_possible_jigsaw_piece_orientations():
    orientations = set(JigsawPieceOrientation.all_possible_orientations())
    assert len(orientations) == 8


@pytest.mark.parametrize(
    "num_quarter_turns, is_flipped, new_position, expected_original_position",
    [
        (0, False, Vector2D(2, 2), Vector2D(2, 2)),
        (0, False, Vector2D(0, 0), Vector2D(0, 0)),
        (0, False, Vector2D(3, 4), Vector2D(3, 4)),
        (1, False, Vector2D(2, 2), Vector2D(2, 2)),
        (1, False, Vector2D(0, 0), Vector2D(0, 4)),
        (1, False, Vector2D(3, 4), Vector2D(4, 1)),
        (2, False, Vector2D(2, 2), Vector2D(2, 2)),
        (2, False, Vector2D(0, 0), Vector2D(4, 4)),
        (2, False, Vector2D(3, 4), Vector2D(1, 0)),
        (3, False, Vector2D(2, 2), Vector2D(2, 2)),
        (3, False, Vector2D(0, 0), Vector2D(4, 0)),
        (3, False, Vector2D(3, 4), Vector2D(0, 3)),
        (0, True, Vector2D(2, 2), Vector2D(2, 2)),
        (0, True, Vector2D(0, 0), Vector2D(4, 0)),
        (0, True, Vector2D(3, 4), Vector2D(1, 4)),
        (1, True, Vector2D(2, 2), Vector2D(2, 2)),
        (1, True, Vector2D(0, 0), Vector2D(4, 4)),
        (1, True, Vector2D(3, 4), Vector2D(0, 1)),
        (2, True, Vector2D(2, 2), Vector2D(2, 2)),
        (2, True, Vector2D(0, 0), Vector2D(0, 4)),
        (2, True, Vector2D(3, 4), Vector2D(3, 0)),
        (3, True, Vector2D(2, 2), Vector2D(2, 2)),
        (3, True, Vector2D(0, 0), Vector2D(0, 0)),
        (3, True, Vector2D(3, 4), Vector2D(4, 3)),
    ],
)
def test_jigsaw_piece_orientation_transforms_position(
    num_quarter_turns, is_flipped, new_position, expected_original_position
):
    center = (2, 2)
    orientation = JigsawPieceOrientation(num_quarter_turns, is_flipped)
    assert (
        orientation.original_position(
            new_position=new_position, center_of_rotation=center
        )
        == expected_original_position
    )


class _MockPiece:
    def __init__(self, piece_id: str = "A", expected_solve_config: str = "") -> None:
        self._piece_id = piece_id
        self._expected_solve_config = expected_solve_config

    @property
    def _expected_position(self) -> Vector2D:
        lines = self._expected_solve_config.split("\n")
        for row, line in enumerate(lines):
            if self._piece_id in line:
                return Vector2D(line.index(self._piece_id), row)

    def __repr__(self) -> str:
        return self._piece_id

    @property
    def piece_id(self) -> Hashable:
        return self._piece_id

    def reorient(self, orientation: JigsawPieceOrientation) -> None:
        pass

    def can_place_other(
        self, other: JigsawPiece, relative_placement: CardinalDirection
    ) -> bool:
        my_pos = self._expected_position
        other_pos = my_pos.move(relative_placement)
        return other_pos == other._expected_position


def test_jigsaw_with_zero_pieces_returns_empty_solution():
    solution = solve_jigsaw(pieces=[])
    assert solution.placed_pieces == dict()


def test_jigsaw_with_one_piece_returns_solution_with_piece_in_origin():
    piece = _MockPiece()
    solution = solve_jigsaw(pieces=[piece])
    assert solution.placed_pieces == {Vector2D(0, 0): piece}


def test_jigsaw_with_multiple_pieces_them_assembles_solution_assuming_maximum_of_one_match_per_edge():
    expected_solution = "ABCD\nEFGH\nIJKL"
    pieces = [
        _MockPiece(piece_id=c, expected_solve_config=expected_solution)
        for c in "ABCDEFGHIJKL"
    ]
    seed(0)
    shuffle(pieces)
    solution = solve_jigsaw(pieces)
    solution_ids = {
        position: piece.piece_id for position, piece in solution.placed_pieces.items()
    }
    assert solution_ids == {
        Vector2D(0, 0): "A",
        Vector2D(1, 0): "B",
        Vector2D(2, 0): "C",
        Vector2D(3, 0): "D",
        Vector2D(0, 1): "E",
        Vector2D(1, 1): "F",
        Vector2D(2, 1): "G",
        Vector2D(3, 1): "H",
        Vector2D(0, 2): "I",
        Vector2D(1, 2): "J",
        Vector2D(2, 2): "K",
        Vector2D(3, 2): "L",
    }


def test_solved_jigsaw_iterates_through_border_pieces():
    placed_pieces = {
        Vector2D(0, 0): _MockPiece(piece_id="A"),
        Vector2D(1, 0): _MockPiece(piece_id="B"),
        Vector2D(2, 0): _MockPiece(piece_id="C"),
        Vector2D(3, 0): _MockPiece(piece_id="D"),
        Vector2D(0, 1): _MockPiece(piece_id="E"),
        Vector2D(1, 1): _MockPiece(piece_id="F"),
        Vector2D(2, 1): _MockPiece(piece_id="G"),
        Vector2D(3, 1): _MockPiece(piece_id="H"),
        Vector2D(0, 2): _MockPiece(piece_id="I"),
        Vector2D(1, 2): _MockPiece(piece_id="J"),
        Vector2D(2, 2): _MockPiece(piece_id="K"),
        Vector2D(3, 2): _MockPiece(piece_id="L"),
    }
    jigsaw = SolvedJigsaw(placed_pieces)
    border_pieces = list(jigsaw.border_pieces())
    assert len(border_pieces) == 4
    assert {piece.piece_id for piece in border_pieces} == {"A", "D", "I", "L"}


def test_jigsaw_piece_binary_image_can_be_constructed_from_and_converted_to_string():
    piece = JigsawPieceBinaryImage(piece_id=0, image_rows=["#..", "#.#"])
    assert piece.width == 3
    assert piece.height == 2
    assert piece.render() == "#..\n#.#"


def test_jigsaw_piece_binary_image_can_be_reoriented():
    piece = JigsawPieceBinaryImage(
        piece_id=0,
        image_rows=[
            "#..",
            "###",
            ".#.",
        ],
    )

    expected_renders = [
        [
            "#..",
            "###",
            ".#.",
        ],
        [
            ".##",
            "##.",
            ".#.",
        ],
        [
            ".#.",
            "###",
            "..#",
        ],
        [
            ".#.",
            ".##",
            "##.",
        ],
        [
            "..#",
            "###",
            ".#.",
        ],
        [
            ".#.",
            "##.",
            ".##",
        ],
        [
            ".#.",
            "###",
            "#..",
        ],
        [
            "##.",
            ".##",
            ".#.",
        ],
    ]

    expected_idx = 0
    for flipped in (False, True):
        for num_quarter_turns in range(4):
            piece.reorient(JigsawPieceOrientation(num_quarter_turns, flipped))
            assert piece.render() == "\n".join(expected_renders[expected_idx])
            expected_idx += 1


def test_jigsaw_pieces_binary_image_do_not_fit_if_different_bits_along_edges():
    piece_a = JigsawPieceBinaryImage(
        piece_id=0,
        image_rows=[
            "#..",
            "###",
            ".#.",
        ],
    )
    piece_b = JigsawPieceBinaryImage(
        piece_id=1,
        image_rows=[
            ".#.",
            "###",
            "..#",
        ],
    )
    assert not piece_a.can_place_other(piece_b, CardinalDirection.NORTH)
    assert not piece_a.can_place_other(piece_b, CardinalDirection.WEST)


def test_jigsaw_pieces_binary_image_fit_if_same_bits_along_edges():
    piece_a = JigsawPieceBinaryImage(
        piece_id=0,
        image_rows=[
            "#..",
            "###",
            ".#.",
        ],
    )
    piece_b = JigsawPieceBinaryImage(
        piece_id=1,
        image_rows=[
            ".#.",
            "###",
            "..#",
        ],
    )
    assert piece_a.can_place_other(piece_b, CardinalDirection.SOUTH)
    assert piece_a.can_place_other(piece_b, CardinalDirection.EAST)
    piece_b.reorient(JigsawPieceOrientation(num_quarter_turns=2, is_flipped=True))
    assert piece_a.can_place_other(piece_b, CardinalDirection.WEST)


def test_solve_jigsaw_with_binary_image_pieces():
    pieces = [
        JigsawPieceBinaryImage(
            piece_id=2311,
            image_rows=[
                "..##.#..#.",
                "##..#.....",
                "#...##..#.",
                "####.#...#",
                "##.##.###.",
                "##...#.###",
                ".#.#.#..##",
                "..#....#..",
                "###...#.#.",
                "..###..###",
            ],
        ),
        JigsawPieceBinaryImage(
            piece_id=1951,
            image_rows=[
                "#.##...##.",
                "#.####...#",
                ".....#..##",
                "#...######",
                ".##.#....#",
                ".###.#####",
                "###.##.##.",
                ".###....#.",
                "..#.#..#.#",
                "#...##.#..",
            ],
        ),
        JigsawPieceBinaryImage(
            piece_id=1171,
            image_rows=[
                "####...##.",
                "#..##.#..#",
                "##.#..#.#.",
                ".###.####.",
                "..###.####",
                ".##....##.",
                ".#...####.",
                "#.##.####.",
                "####..#...",
                ".....##...",
            ],
        ),
        JigsawPieceBinaryImage(
            piece_id=1427,
            image_rows=[
                "###.##.#..",
                ".#..#.##..",
                ".#.##.#..#",
                "#.#.#.##.#",
                "....#...##",
                "...##..##.",
                "...#.#####",
                ".#.####.#.",
                "..#..###.#",
                "..##.#..#.",
            ],
        ),
        JigsawPieceBinaryImage(
            piece_id=1489,
            image_rows=[
                "##.#.#....",
                "..##...#..",
                ".##..##...",
                "..#...#...",
                "#####...#.",
                "#..#.#.#.#",
                "...#.#.#..",
                "##.#...##.",
                "..##.##.##",
                "###.##.#..",
            ],
        ),
        JigsawPieceBinaryImage(
            piece_id=2473,
            image_rows=[
                "#....####.",
                "#..#.##...",
                "#.##..#...",
                "######.#.#",
                ".#...#.#.#",
                ".#########",
                ".###.#..#.",
                "########.#",
                "##...##.#.",
                "..###.#.#.",
            ],
        ),
        JigsawPieceBinaryImage(
            piece_id=2971,
            image_rows=[
                "..#.#....#",
                "#...###...",
                "#.#.###...",
                "##.##..#..",
                ".#####..##",
                ".#..####.#",
                "#..#.#..#.",
                "..####.###",
                "..#.#.###.",
                "...#.#.#.#",
            ],
        ),
        JigsawPieceBinaryImage(
            piece_id=2729,
            image_rows=[
                "...#.#.#.#",
                "####.#....",
                "..#.#.....",
                "....#..#.#",
                ".##..##.#.",
                ".#.####...",
                "####.#.#..",
                "##.####...",
                "##..#.##..",
                "#.##...##.",
            ],
        ),
        JigsawPieceBinaryImage(
            piece_id=3079,
            image_rows=[
                "#.#.#####.",
                ".#..######",
                "..#.......",
                "######....",
                "####.#..#.",
                ".#...#.##.",
                "#.#####.##",
                "..#.###...",
                "..#.......",
                "..#.###...",
            ],
        ),
    ]
    solution = solve_jigsaw(pieces)
    border_ids = {piece.piece_id for piece in solution.border_pieces()}
    assert border_ids == {1951, 3079, 2971, 1171}
