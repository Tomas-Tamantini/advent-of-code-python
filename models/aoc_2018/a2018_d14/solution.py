from models.common.io import InputReader, ProgressBarConsole
from .hot_chocolate import HotChocolateRecipeScores


def aoc_2018_d14(
    input_reader: InputReader, progress_bar: ProgressBarConsole, **_
) -> None:
    print("--- AOC 2018 - Day 14: Chocolate Charts ---")
    num_steps = int(input_reader.read())
    recipe_scores = HotChocolateRecipeScores(first_score=3, second_score=7)
    score_generator = recipe_scores.generate_scores()
    first_scores = [next(score_generator) for _ in range(num_steps + 10)]
    last_ten_scores = "".join(map(str, first_scores[num_steps : num_steps + 10]))
    print(f"Part 1: Scores of next 10 recipes: {last_ten_scores}")
    first_occurrence = recipe_scores.first_occurrence_of_subsequence(
        tuple(map(int, str(num_steps))), progress_bar
    )
    print(
        f"Part 2: Number of recipes to the left of the score sequence: {first_occurrence}"
    )