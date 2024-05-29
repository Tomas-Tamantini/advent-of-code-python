from ..cookie import CookieProperties, CookieRecipe


def test_recipe_with_single_ingredient_uses_only_that_ingredient():
    ingredients = [CookieProperties(1, 2, 3, 4, 5)]
    recipe = CookieRecipe(ingredients, num_tablespoons=10)
    assert recipe.optimal_recipe() == CookieProperties(10, 20, 30, 40, 50)


def test_negative_properties_are_set_to_zero_in_final_recipe():
    ingredients = [CookieProperties(1, -2, 3, 4, 5)]
    recipe = CookieRecipe(ingredients, num_tablespoons=10)
    assert recipe.optimal_recipe() == CookieProperties(10, 0, 30, 40, 50)


def test_recipe_is_chosen_to_maximize_product_of_properties_except_calories():
    ingredients = [
        CookieProperties(-1, -2, 6, 3, 8),
        CookieProperties(2, 3, -2, -1, 3),
    ]
    recipe = CookieRecipe(ingredients, num_tablespoons=100)
    assert recipe.optimal_recipe() == CookieProperties(68, 80, 152, 76, 520)


def test_optimal_recipe_can_have_specified_calories_amount():
    ingredients = [
        CookieProperties(-1, -2, 6, 3, 8),
        CookieProperties(2, 3, -2, -1, 3),
    ]
    recipe = CookieRecipe(ingredients, num_tablespoons=100)
    assert recipe.optimal_recipe(num_calories=500).score() == 57_600_000
