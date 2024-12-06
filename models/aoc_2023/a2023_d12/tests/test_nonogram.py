import pytest

from ..logic import NonogramRow, num_arrangements_nonogram_row


@pytest.mark.parametrize(
    "cells, contiguous_groups_size, num_arrangements",
    [
        (".", (1,), 0),
        ("###", (3,), 1),
        ("???#??", (3,), 3),
        ("??.??", (1, 1), 4),
        ("???.###", (1, 1, 3), 1),
        (".??..??...?##.", (1, 1, 3), 4),
        ("?#?#?#?#?#?#?#?", (1, 3, 1, 6), 1),
        ("????.#...#...", (4, 1, 1), 1),
        ("????.######..#####.", (1, 6, 5), 4),
        ("?###????????", (3, 2, 1), 10),
    ],
)
def test_nonogram_row_returns_number_of_possible_arrangements(
    cells, contiguous_groups_size, num_arrangements
):
    row = NonogramRow(cells, contiguous_groups_size)
    assert num_arrangements_nonogram_row(row) == num_arrangements


def test_nonogram_row_calculates_arrangements_efficiently():
    num_groups = 20
    cells = "??." * num_groups
    groups = tuple([1] * num_groups)
    row = NonogramRow(cells, groups)
    assert num_arrangements_nonogram_row(row) == 2**num_groups
