import numpy as np
from ..bingo import BingoBoard, BingoGame


def test_bingo_board_has_dimensions_equal_to_its_input_matrix():
    input_matrix = np.array([[1, 2], [3, 4], [5, 6]])
    bingo_board = BingoBoard(numbers_table=input_matrix)
    assert bingo_board.num_rows == 3
    assert bingo_board.num_columns == 2


table = np.array(
    [
        [14, 21, 17, 24, 4],
        [10, 16, 15, 9, 19],
        [18, 8, 23, 26, 20],
        [22, 11, 13, 6, 5],
        [2, 0, 12, 3, 7],
    ]
)


def test_bingo_board_starts_with_all_unmarked_numbers():
    board = BingoBoard(numbers_table=table)
    assert len(list(board.unmarked_numbers())) == 25


def test_number_marked_in_bingo_board_gets_recorded():
    board = BingoBoard(numbers_table=table)
    board.mark_number(23)
    unmarked = list(board.unmarked_numbers())
    assert 23 not in unmarked
    assert len(unmarked) == 24


def test_empty_bingo_board_is_not_winner():
    board = BingoBoard(numbers_table=table)
    assert not board.is_winner()


def test_bingo_board_is_winner_if_row_is_marked():
    board = BingoBoard(numbers_table=table)
    for number in [22, 11, 13, 6, 5]:
        board.mark_number(number)
    assert board.is_winner()


def test_bingo_board_is_winner_if_column_is_marked():
    board = BingoBoard(numbers_table=table)
    for number in [21, 16, 8, 11, 0]:
        board.mark_number(number)
    assert board.is_winner()


def test_bingo_board_is_not_winner_if_diagonal_is_marked():
    board = BingoBoard(numbers_table=table)
    for number in [14, 16, 23, 6, 7]:
        board.mark_number(number)
    assert not board.is_winner()


def test_bingo_game_keeps_track_of_whether_there_is_some_winner():
    board_a = BingoBoard(
        np.array(
            [
                [22, 13, 17, 11, 0],
                [8, 2, 23, 4, 24],
                [21, 9, 14, 16, 7],
                [6, 10, 3, 18, 5],
                [1, 12, 20, 15, 19],
            ]
        )
    )
    board_b = BingoBoard(
        np.array(
            [
                [3, 15, 0, 2, 22],
                [9, 18, 13, 17, 5],
                [19, 8, 7, 25, 23],
                [20, 11, 10, 24, 4],
                [14, 21, 16, 12, 6],
            ]
        )
    )
    board_c = BingoBoard(table)
    game = BingoGame((board_a, board_b, board_c))
    assert not game.some_winner()
    for number in [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24]:
        game.draw_number(number)
    assert game.some_winner()
    assert game.winners == [board_c]


def test_bingo_game_keeps_track_of_whether_every_board_won_and_stores_them_in_the_order_which_they_won():
    board_a = BingoBoard(
        np.array(
            [
                [22, 13, 17, 11, 0],
                [8, 2, 23, 4, 24],
                [21, 9, 14, 16, 7],
                [6, 10, 3, 18, 5],
                [1, 12, 20, 15, 19],
            ]
        )
    )
    board_b = BingoBoard(
        np.array(
            [
                [3, 15, 0, 2, 22],
                [9, 18, 13, 17, 5],
                [19, 8, 7, 25, 23],
                [20, 11, 10, 24, 4],
                [14, 21, 16, 12, 6],
            ]
        )
    )
    board_c = BingoBoard(table)
    game = BingoGame((board_a, board_b, board_c))
    assert not game.all_boards_won()
    for number in [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10, 16, 13]:
        game.draw_number(number)
    assert game.all_boards_won()
    assert game.winners == [board_c, board_a, board_b]
