from collections import defaultdict
from typing import Iterator


class PolymerExtension:
    def __init__(self, rules: dict[str, str]) -> None:
        self._rules = rules

    def extend(self, polymer: str) -> str:
        extended = ""
        for i in range(len(polymer) - 1):
            pair = polymer[i : i + 2]
            if pair in self._rules:
                extended += polymer[i] + self._rules[pair]
            else:
                extended += polymer[i]
        if len(polymer) > 0:
            extended += polymer[-1]
        return extended

    @staticmethod
    def _pairs(polymer: str) -> Iterator[str]:
        for i in range(len(polymer) - 1):
            yield polymer[i : i + 2]

    @staticmethod
    def _increment_character_count(
        total_count: dict[chr, int], new_count: dict[chr, int]
    ) -> None:
        for character, count in new_count.items():
            total_count[character] += count

    def _character_count_recursive(
        self,
        pair: str,
        num_times: int,
        memoized_results: dict[tuple[str, int], dict[str, int]],
    ) -> dict[chr, int]:
        if num_times == 0 or pair not in self._rules:
            return dict()
        if (pair, num_times) in memoized_results:
            return memoized_results[(pair, num_times)]
        count = defaultdict(int)
        inserted = self._rules[pair]
        count[inserted] += 1
        for character_pair in self._pairs(pair[0] + inserted + pair[1]):
            pair_count = self._character_count_recursive(
                character_pair, num_times - 1, memoized_results
            )
            self._increment_character_count(count, pair_count)
        memoized_results[(pair, num_times)] = count
        return count

    def character_count_after_multiple_extensions(
        self, polymer: str, num_times: int
    ) -> dict[chr, int]:
        count = defaultdict(int)
        memoized_results = dict()
        for character_pair in self._pairs(polymer):
            count[character_pair[0]] += 1
            pair_count = self._character_count_recursive(
                character_pair, num_times, memoized_results
            )
            self._increment_character_count(count, pair_count)
        if len(polymer) > 0:
            count[polymer[-1]] += 1
        return count
