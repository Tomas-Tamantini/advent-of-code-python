from models.common.io import IOHandler, Problem
from .parser import parse_bingo_game_and_numbers_to_draw


def aoc_2021_d4(io_handler: IOHandler) -> None:
    problem_id = Problem(2021, 4, "Giant Squid")
    io_handler.output_writer.write_header(problem_id)
    game, numbers_to_draw = parse_bingo_game_and_numbers_to_draw(
        io_handler.input_reader
    )
    product_first_winner = -1
    product_last_winner = -1
    for number in numbers_to_draw:
        game.draw_number(number)
        if product_first_winner == -1 and game.some_winner():
            product_first_winner = number * sum(game.winners[0].unmarked_numbers())
        elif game.all_boards_won():
            product_last_winner = number * sum(game.winners[-1].unmarked_numbers())
            break
    print(f"Part 1: The product for the first bingo winner is {product_first_winner}")
    print(f"Part 2: The product for the last bingo winner is {product_last_winner}")
