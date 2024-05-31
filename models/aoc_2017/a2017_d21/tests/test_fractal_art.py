import numpy as np
from ..fractal_art import ArtBlock, FractalArt


def _build_art_block(pattern: list[list[int]]) -> ArtBlock:
    return ArtBlock(np.array(pattern))


def test_art_blocks_with_different_patterns_are_different():
    block_a = _build_art_block([[1, 0], [0, 1]])
    block_b = _build_art_block([[1, 0], [1, 0]])
    assert block_a != block_b
    assert hash(block_a) != hash(block_b)


def test_art_block_is_equivalent_under_rotation_and_reflection():
    equivalent_patterns = [
        np.array([[1, 1, 0], [0, 0, 0], [0, 0, 0]]),
        np.array([[0, 1, 1], [0, 0, 0], [0, 0, 0]]),
        np.array([[0, 0, 0], [0, 0, 0], [0, 1, 1]]),
        np.array([[0, 0, 0], [0, 0, 0], [1, 1, 0]]),
        np.array([[0, 0, 1], [0, 0, 1], [0, 0, 0]]),
        np.array([[0, 0, 0], [0, 0, 1], [0, 0, 1]]),
        np.array([[1, 0, 0], [1, 0, 0], [0, 0, 0]]),
        np.array([[0, 0, 0], [1, 0, 0], [1, 0, 0]]),
    ]
    ref_block = ArtBlock(equivalent_patterns[0])
    for pattern in equivalent_patterns:
        block = ArtBlock(pattern)
        assert block == ref_block
        assert hash(block) == hash(ref_block)


def test_subdividing_2x2_block_into_2x2_subblocks_returns_same_block():
    block = _build_art_block([[1, 0], [0, 1]])
    assert list(block.subdivide(size=2)) == [block]


def test_subdividing_6x6_block_into_3x3_subblocks_returns_4_3x3_blocks():
    block = ArtBlock(
        np.array(
            [
                [1, 1, 1, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [0, 1, 0, 1, 0, 1],
                [1, 0, 1, 0, 1, 0],
                [0, 1, 0, 1, 0, 1],
            ]
        )
    )
    subblocks = list(block.subdivide(size=3))
    assert len(subblocks) == 4
    assert subblocks[0] == _build_art_block([[1, 1, 1], [1, 1, 1], [1, 1, 1]])
    assert subblocks[1] == _build_art_block([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    assert subblocks[2] == _build_art_block([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    assert subblocks[3] == _build_art_block([[1, 0, 1], [0, 1, 0], [1, 0, 1]])


def test_can_calculate_number_of_cells_that_are_on_after_n_iterations():
    initial_pattern = _build_art_block([[0, 1, 0], [0, 0, 1], [1, 1, 1]])
    rules = {
        _build_art_block([[0, 0], [0, 1]]): _build_art_block(
            [[1, 1, 0], [1, 0, 0], [0, 0, 0]]
        ),
        _build_art_block([[0, 0], [0, 0]]): _build_art_block(
            [[1, 0, 0], [1, 0, 0], [0, 0, 0]]
        ),
        _build_art_block([[1, 1], [0, 1]]): _build_art_block(
            [[1, 0, 0], [0, 0, 0], [0, 0, 0]]
        ),
        _build_art_block([[0, 0], [1, 1]]): _build_art_block(
            [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
        ),
        _build_art_block([[0, 1, 0], [0, 0, 1], [1, 1, 1]]): _build_art_block(
            [[1, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 1]]
        ),
    }
    fractal_art = FractalArt(initial_pattern, rules)
    assert fractal_art.num_cells_on_after_iterations(0) == 5
    assert fractal_art.num_cells_on_after_iterations(1) == 4
    assert fractal_art.num_cells_on_after_iterations(2) == 12
    assert fractal_art.num_cells_on_after_iterations(3) == 36


def test_fractal_art_iterations_are_run_efficiently():
    initial_pattern = _build_art_block([[0, 0], [0, 0]])
    rules = {
        _build_art_block([[0, 0], [0, 0]]): _build_art_block(
            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        ),
        _build_art_block([[0, 0, 0], [0, 0, 0], [0, 0, 0]]): _build_art_block(
            [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        ),
    }
    fractal_art = FractalArt(initial_pattern, rules)
    assert fractal_art.num_cells_on_after_iterations(20) == 0
