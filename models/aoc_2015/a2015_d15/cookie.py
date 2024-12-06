from dataclasses import dataclass
from itertools import combinations
from typing import Iterator, Optional


@dataclass(frozen=True)
class CookieProperties:
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    def multiply_by_tablespoons(self, num_tablespoons: int) -> "CookieProperties":
        return CookieProperties(
            capacity=self.capacity * num_tablespoons,
            durability=self.durability * num_tablespoons,
            flavor=self.flavor * num_tablespoons,
            texture=self.texture * num_tablespoons,
            calories=self.calories * num_tablespoons,
        )

    def remove_negative_properties(self) -> "CookieProperties":
        return CookieProperties(
            capacity=max(self.capacity, 0),
            durability=max(self.durability, 0),
            flavor=max(self.flavor, 0),
            texture=max(self.texture, 0),
            calories=max(self.calories, 0),
        )

    @staticmethod
    def add_properties(*properties: "CookieProperties") -> "CookieProperties":
        return CookieProperties(
            capacity=sum(p.capacity for p in properties),
            durability=sum(p.durability for p in properties),
            flavor=sum(p.flavor for p in properties),
            texture=sum(p.texture for p in properties),
            calories=sum(p.calories for p in properties),
        )

    def score(self) -> int:
        return self.capacity * self.durability * self.flavor * self.texture


class CookieRecipe:
    def __init__(
        self,
        ingredients: list[CookieProperties],
        num_tablespoons: int,
    ) -> None:
        self._ingredients = ingredients
        self._num_tablespoons = num_tablespoons

    def _possible_proportions(self) -> Iterator[list[int]]:
        num_walls = len(self._ingredients) - 1
        num_possible_indices = num_walls + self._num_tablespoons
        for comb in combinations(range(num_possible_indices), num_walls):
            if (len(comb)) == 0:
                yield [self._num_tablespoons]
            else:
                yield (
                    [comb[0]]
                    + [comb[i] - comb[i - 1] - 1 for i in range(1, num_walls)]
                    + [num_possible_indices - comb[-1] - 1]
                )

    def _recipe(self, proportion: list[int]) -> CookieProperties:
        multiplied_ingredients = [
            ingredient.multiply_by_tablespoons(prop)
            for prop, ingredient in zip(proportion, self._ingredients)
        ]
        recipe = CookieProperties.add_properties(*multiplied_ingredients)
        return recipe.remove_negative_properties()

    def optimal_recipe(self, num_calories: Optional[int] = None) -> CookieProperties:
        best_recipe = None
        best_score = -1
        for proportion in self._possible_proportions():
            recipe = self._recipe(proportion)
            if num_calories is not None and recipe.calories != num_calories:
                continue
            score = recipe.score()
            if score > best_score:
                best_score = score
                best_recipe = recipe
        return best_recipe
