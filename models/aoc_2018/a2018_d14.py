from typing import Iterator


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
