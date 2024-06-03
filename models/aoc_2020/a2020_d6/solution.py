from models.common.io import InputReader
from .parser import parse_form_answers_by_groups


def aoc_2020_d6(input_reader: InputReader, **_) -> None:
    print("--- AOC 2020 - Day 6: Custom Customs ---")
    groups = list(parse_form_answers_by_groups(input_reader))
    union_yes = sum(len(group.questions_with_at_least_one_yes()) for group in groups)
    print(f"Part 1: The sum of union 'yes' answers is {union_yes}")

    intersection_yes = sum(
        len(group.questions_everyone_answered_yes()) for group in groups
    )
    print(f"Part 2: The sum of intersection 'yes' answers is {intersection_yes}")
