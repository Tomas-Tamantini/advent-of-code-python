from ..foods import Food, Foods


def test_foods_keep_track_of_how_many_times_ingredient_appears():
    foods = Foods(
        [
            Food(ingredients={"a", "b", "c"}, allergens=set()),
            Food(ingredients={"a", "b", "d"}, allergens=set()),
        ]
    )
    assert foods.num_times_ingredient_appears("a") == 2
    assert foods.num_times_ingredient_appears("b") == 2
    assert foods.num_times_ingredient_appears("c") == 1
    assert foods.num_times_ingredient_appears("d") == 1
    assert foods.num_times_ingredient_appears("e") == 0


def test_foods_deduce_which_ingredients_cannot_have_allergens():
    foods = Foods(
        [
            Food(
                ingredients={"mxmxvkd", "kfcds", "sqjhc", "nhms"},
                allergens={"dairy", "fish"},
            ),
            Food(ingredients={"trh", "fvjkl", "sbzzf", "mxmxvkd"}, allergens={"dairy"}),
            Food(ingredients={"sqjhc", "fvjkl"}, allergens={"soy"}),
            Food(ingredients={"sqjhc", "mxmxvkd", "sbzzf"}, allergens={"fish"}),
        ]
    )
    assert foods.ingredients_without_allergens() == {"kfcds", "nhms", "sbzzf", "trh"}


def test_foods_deduce_which_ingredients_must_have_allergens():
    foods = Foods(
        [
            Food(
                ingredients={"mxmxvkd", "kfcds", "sqjhc", "nhms"},
                allergens={"dairy", "fish"},
            ),
            Food(ingredients={"trh", "fvjkl", "sbzzf", "mxmxvkd"}, allergens={"dairy"}),
            Food(ingredients={"sqjhc", "fvjkl"}, allergens={"soy"}),
            Food(ingredients={"sqjhc", "mxmxvkd", "sbzzf"}, allergens={"fish"}),
        ]
    )
    assert foods.ingredients_with_allergens() == {
        "mxmxvkd": "dairy",
        "sqjhc": "fish",
        "fvjkl": "soy",
    }
