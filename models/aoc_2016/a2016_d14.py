from typing import Iterator
from dataclasses import dataclass
from hashlib import md5
from bisect import insort


@dataclass
class _KeyCandidate:
    index: int
    hashed_value: str
    repeated_character: chr


class KeyGenerator:
    def __init__(
        self,
        salt: str,
        num_repeated_characters_first_occurrence: int,
        num_repeated_characters_second_occurrence: int,
        max_num_steps_between_occurrences: int,
        num_hashes: int = 1,
    ) -> None:
        self._salt = salt
        self._num_repeated_characters_first_occurrence = (
            num_repeated_characters_first_occurrence
        )
        self._num_repeated_characters_second_occurrence = (
            num_repeated_characters_second_occurrence
        )
        self._max_num_steps_between_occurrences = max_num_steps_between_occurrences
        self._num_hashes = num_hashes

    @staticmethod
    def _split_along_character_changes(string: str) -> Iterator[str]:
        previous_character = None
        current_string = ""
        for character in string:
            if character != previous_character:
                if current_string:
                    yield current_string
                current_string = ""
            current_string += character
            previous_character = character
        if current_string:
            yield current_string

    def _hash_value(self, index: int) -> str:
        message = self._salt + str(index)
        for _ in range(self._num_hashes):
            message = md5(message.encode()).hexdigest()
        return message

    def _grouping_is_big_enough_to_be_a_key(self, grouping: str) -> bool:
        return len(grouping) >= self._num_repeated_characters_first_occurrence

    def _grouping_is_big_enough_to_match_a_key(self, grouping: str) -> bool:
        return len(grouping) >= self._num_repeated_characters_second_occurrence

    def _analyse_index(
        self, index: int, candidates: list[_KeyCandidate]
    ) -> Iterator[int]:
        hashed_value = self._hash_value(index)
        repeated_character = ""
        for character_grouping in self._split_along_character_changes(hashed_value):
            if not repeated_character and (
                self._grouping_is_big_enough_to_be_a_key(character_grouping)
            ):
                repeated_character = character_grouping[0]
            if self._grouping_is_big_enough_to_match_a_key(character_grouping):
                candidates_to_remove = []
                for candidate in candidates:
                    if self._candidate_is_outside_window(index, candidate):
                        candidates_to_remove.append(candidate)
                    elif character_grouping[0] == candidate.repeated_character:
                        yield candidate.index
                        candidates_to_remove.append(candidate)
                for candidate in candidates_to_remove:
                    candidates.remove(candidate)

        if repeated_character:
            candidates.append(_KeyCandidate(index, hashed_value, repeated_character))

    def _candidate_is_outside_window(self, index, candidate):
        return candidate.index < index - self._max_num_steps_between_occurrences

    def _indices_which_produce_keys(self) -> Iterator[int]:
        candidates: list[_KeyCandidate] = []
        index = 0
        while True:
            yield from self._analyse_index(index, candidates)
            index += 1

    def indices_which_produce_keys(self, num_indices: int) -> list[int]:
        sorted_indices = []
        for index in self._indices_which_produce_keys():
            insort(sorted_indices, index)
            if (
                len(sorted_indices) >= num_indices
                and index
                > sorted_indices[num_indices - 1]
                + self._max_num_steps_between_occurrences
            ):
                break
        return sorted_indices[:num_indices]
