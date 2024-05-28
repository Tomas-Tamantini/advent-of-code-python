import pytest
from .hot_chocolate import HotChocolateRecipeScores


def test_hot_chocolate_recipe_scores_are_calculated_properly():
    score_generator = HotChocolateRecipeScores(
        first_score=3, second_score=7
    ).generate_scores()
    first_scores = [next(score_generator) for _ in range(17)]

    assert first_scores == [3, 7, 1, 0, 1, 0, 1, 2, 4, 5, 1, 5, 8, 9, 1, 6, 7]


@pytest.mark.parametrize(
    "subsequence, expected_position",
    [
        ((5, 1, 5, 8, 9), 9),
        ((0, 1, 2, 4, 5), 5),
        ((9, 2, 5, 1, 0), 18),
        ((5, 9, 4, 1, 4), 2018),
    ],
)
def test_can_find_first_occurrence_of_given_subsequence(subsequence, expected_position):
    score_generator = HotChocolateRecipeScores(first_score=3, second_score=7)
    assert (
        score_generator.first_occurrence_of_subsequence(subsequence)
        == expected_position
    )
