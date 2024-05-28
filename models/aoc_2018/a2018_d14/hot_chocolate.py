from typing import Iterator, Optional
from models.common.io import ProgressBar


class HotChocolateRecipeScores:
    def __init__(self, first_score: int, second_score: int) -> None:
        self._scores = [first_score, second_score]
        self._elf_indices = [0, 1]

    def _generate_next_scores(self) -> Iterator[int]:
        next_scores = sum(self._scores[i] for i in self._elf_indices)
        if next_scores >= 10:
            yield 1
            yield next_scores % 10
            self._scores.extend([1, next_scores % 10])
        else:
            yield next_scores
            self._scores.append(next_scores)
        self._update_elf_indices()

    def _update_elf_indices(self):
        self._elf_indices = [self._next_elf_index(index) for index in self._elf_indices]

    def _next_elf_index(self, index: int) -> int:
        return (index + self._scores[index] + 1) % len(self._scores)

    def generate_scores(self) -> Iterator[int]:
        yield self._scores[0]
        yield self._scores[1]
        while True:
            yield from self._generate_next_scores()

    def first_occurrence_of_subsequence(
        self,
        subsequence: tuple[int, ...],
        progress_bar: Optional[ProgressBar] = None,
    ) -> int:
        self._scores = self._scores[:2]
        self._elf_indices = [0, 1]
        subsequence_length = len(subsequence)
        expected_num_steps = 10 ** (subsequence_length + 1)
        subsequence_index = 0
        for index, score in enumerate(self.generate_scores()):
            if progress_bar is not None:
                progress_bar.update(index, expected_num_steps)
            if score == subsequence[subsequence_index]:
                subsequence_index += 1
                if subsequence_index == subsequence_length:
                    return index - subsequence_length + 1
            else:
                subsequence_index = 0
                if score == subsequence[subsequence_index]:
                    subsequence_index += 1
