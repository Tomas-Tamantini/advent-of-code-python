from models.common.io import InputFromString
from ..parser import parse_foods


def test_parse_foods():
    file_content = """
                   mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
                   trh fvjkl sbzzf mxmxvkd (contains dairy)
                   """
    foods = list(parse_foods(InputFromString(file_content)))
    assert len(foods) == 2
    assert foods[0].ingredients == {"mxmxvkd", "kfcds", "sqjhc", "nhms"}
    assert foods[0].allergens == {"dairy", "fish"}
    assert foods[1].ingredients == {"trh", "fvjkl", "sbzzf", "mxmxvkd"}
    assert foods[1].allergens == {"dairy"}
