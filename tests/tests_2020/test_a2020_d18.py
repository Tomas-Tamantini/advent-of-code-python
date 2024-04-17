from models.aoc_2020 import (
    evaluate_expression_left_precedence,
    evaluate_expression_addition_precedence,
)


def test_evaluation_of_empty_expression_is_zero():
    assert evaluate_expression_left_precedence("") == 0
    assert evaluate_expression_addition_precedence("") == 0


def test_evaluation_of_single_number_is_that_number():
    assert evaluate_expression_left_precedence("123") == 123
    assert evaluate_expression_addition_precedence("123") == 123


def test_evaluation_of_addition_is_sum_of_the_two_numbers():
    assert evaluate_expression_left_precedence("1 + 2") == 3
    assert evaluate_expression_addition_precedence("1 + 2") == 3


def test_evaluation_of_multiplication_is_product_of_the_two_numbers():
    assert evaluate_expression_left_precedence("11 * 13") == 143
    assert evaluate_expression_addition_precedence("11 * 13") == 143


def test_evaluation_of_expression_with_three_or_more_numbers_gives_precedence_to_leftmost_operator():
    assert evaluate_expression_left_precedence("1 + 2 * 3") == 9
    assert evaluate_expression_left_precedence("1 * 2 + 3") == 5
    assert evaluate_expression_left_precedence("1 + 2 * 3 + 4 * 5 + 6") == 71


def test_evaluation_of_expression_with_three_or_more_numbers_gives_precedence_to_addition_operator():
    assert evaluate_expression_addition_precedence("1 + 2 * 3") == 9
    assert evaluate_expression_addition_precedence("2 * 2 + 3") == 10
    assert evaluate_expression_addition_precedence("1 + 2 * 3 + 4 * 5 + 6") == 231


def test_evaluation_of_expression_gives_precedence_to_parentheses():
    assert evaluate_expression_left_precedence("1 + (2 * 3) + 4") == 11
    assert evaluate_expression_left_precedence("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert evaluate_expression_left_precedence("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437

    assert evaluate_expression_addition_precedence("1 + (2 * 3) + 4") == 11
    assert evaluate_expression_addition_precedence("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert (
        evaluate_expression_addition_precedence("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    )
