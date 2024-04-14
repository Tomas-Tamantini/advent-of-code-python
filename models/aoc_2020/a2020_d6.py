class CustomsGroup:
    def __init__(self):
        self._individual_answers = []

    @property
    def answers(self) -> list[set[chr]]:
        return self._individual_answers

    def add_individual_answers(self, answers: set[chr]) -> None:
        self._individual_answers.append(answers)

    def questions_with_at_least_one_yes(self) -> set[chr]:
        return set.union(*self._individual_answers)

    def questions_everyone_answered_yes(self) -> set[chr]:
        return set.intersection(*self._individual_answers)
