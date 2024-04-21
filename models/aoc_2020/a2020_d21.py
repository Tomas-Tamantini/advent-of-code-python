from dataclasses import dataclass
from typing import Iterator, Optional
from enum import Enum
import numpy as np


@dataclass
class Food:
    ingredients: set[str]
    allergens: set[str]


class _MatchStatus(int, Enum):
    UNKNOWN = 0
    MATCHES = 1
    DOES_NOT_MATCH = 2


class _MatchMatrix:
    def __init__(self, ingredients: set[str], allergens: set[str]) -> None:
        self._ingredient_indices = {
            ingredient: idx for idx, ingredient in enumerate(ingredients)
        }
        self._allergen_indices = {
            allergen: idx for idx, allergen in enumerate(allergens)
        }
        num_rows = len(ingredients)
        num_cols = len(allergens)
        self._values = np.full((num_rows, num_cols), _MatchStatus.UNKNOWN)

    @property
    def _num_rows(self) -> int:
        return self._values.shape[0]

    @property
    def _num_cols(self) -> int:
        return self._values.shape[1]

    def _count_status_in_column(self, column_idx: int, status: _MatchStatus) -> int:
        return np.count_nonzero(self._values[:, column_idx] == status)

    def _row_index_of_only_possible_match(self, col_idx: int) -> Optional[int]:
        num_matches = self._count_status_in_column(col_idx, _MatchStatus.MATCHES)
        if num_matches > 0:
            return None
        num_non_matches = self._count_status_in_column(
            col_idx, _MatchStatus.DOES_NOT_MATCH
        )
        if num_non_matches == self._num_rows - 1:
            return np.argmax(self._values[:, col_idx] == _MatchStatus.UNKNOWN)

    def _reduce(self, col_idx: int) -> None:
        row_idx_new_match = self._row_index_of_only_possible_match(col_idx)
        if row_idx_new_match is None:
            return
        self._values[row_idx_new_match, col_idx] = _MatchStatus.MATCHES
        for other_col_idx in range(self._num_cols):
            if other_col_idx != col_idx:
                self._values[row_idx_new_match, other_col_idx] = (
                    _MatchStatus.DOES_NOT_MATCH
                )
                self._reduce(other_col_idx)

    def set_does_not_match(self, ingredient: str, allergen: str) -> None:
        row_idx = self._ingredient_indices[ingredient]
        col_idx = self._allergen_indices[allergen]
        self._values[row_idx, col_idx] = _MatchStatus.DOES_NOT_MATCH
        self._reduce(col_idx)

    def ingredients_without_allergens(self) -> Iterator[str]:
        for ingredient, idx in self._ingredient_indices.items():
            if all(
                status == _MatchStatus.DOES_NOT_MATCH for status in self._values[idx, :]
            ):
                yield ingredient

    def ingredients_with_allergens(self) -> dict[str, str]:
        matches = dict()
        for ingredient, row_idx in self._ingredient_indices.items():
            for allergen, col_idx in self._allergen_indices.items():
                if self._values[row_idx, col_idx] == _MatchStatus.MATCHES:
                    matches[ingredient] = allergen
        return matches


class Foods:
    def __init__(self, foods: list[Food]) -> None:
        self._foods = foods
        self._match_matrix = self._build_match_matrix()

    def num_times_ingredient_appears(self, ingredient: str) -> int:
        return sum(ingredient in food.ingredients for food in self._foods)

    def _all_ingredients(self) -> set[str]:
        return set(
            ingredient for food in self._foods for ingredient in food.ingredients
        )

    def _all_allergens(self) -> set[str]:
        return set(allergen for food in self._foods for allergen in food.allergens)

    def _build_match_matrix(self) -> _MatchMatrix:
        all_ingredients = self._all_ingredients()
        matrix = _MatchMatrix(
            ingredients=self._all_ingredients(), allergens=self._all_allergens()
        )
        for food in self._foods:
            for ingredient in all_ingredients - food.ingredients:
                for allergen in food.allergens:
                    matrix.set_does_not_match(ingredient, allergen)
        return matrix

    def ingredients_without_allergens(self) -> set[str]:
        return set(self._match_matrix.ingredients_without_allergens())

    def ingredients_with_allergens(self) -> dict[str, str]:
        return self._match_matrix.ingredients_with_allergens()
