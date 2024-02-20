import pytest
from models.aoc_2019 import ChemicalQuantity, ChemicalReaction, ChemicalReactions


def test_chemical_reaction_calculates_inputs_required_to_produce_given_output():
    reaction = ChemicalReaction(
        inputs=(
            ChemicalQuantity(chemical="A", quantity=10),
            ChemicalQuantity(chemical="B", quantity=20),
        ),
        output=ChemicalQuantity(chemical="C", quantity=30),
    )
    assert reaction.inputs_required_to_produce_output(quantity=63) == (
        ChemicalQuantity(chemical="A", quantity=30),
        ChemicalQuantity(chemical="B", quantity=60),
    )


reactions_a = ChemicalReactions(
    {
        ChemicalReaction(
            inputs=(ChemicalQuantity("ORE", 10),),
            output=ChemicalQuantity("A", 10),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("ORE", 1),),
            output=ChemicalQuantity("B", 1),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("A", 7), ChemicalQuantity("B", 1)),
            output=ChemicalQuantity("C", 1),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("A", 7), ChemicalQuantity("C", 1)),
            output=ChemicalQuantity("D", 1),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("A", 7), ChemicalQuantity("D", 1)),
            output=ChemicalQuantity("E", 1),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("A", 7), ChemicalQuantity("E", 1)),
            output=ChemicalQuantity("FUEL", 1),
        ),
    }
)

reactions_b = ChemicalReactions(
    {
        ChemicalReaction(
            inputs=(ChemicalQuantity("ORE", 9),),
            output=ChemicalQuantity("A", 2),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("ORE", 8),),
            output=ChemicalQuantity("B", 3),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("ORE", 7),),
            output=ChemicalQuantity("C", 5),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("A", 3), ChemicalQuantity("B", 4)),
            output=ChemicalQuantity("AB", 1),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("B", 5), ChemicalQuantity("C", 7)),
            output=ChemicalQuantity("BC", 1),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("C", 4), ChemicalQuantity("A", 1)),
            output=ChemicalQuantity("CA", 1),
        ),
        ChemicalReaction(
            inputs=(
                ChemicalQuantity("AB", 2),
                ChemicalQuantity("BC", 3),
                ChemicalQuantity("CA", 4),
            ),
            output=ChemicalQuantity("FUEL", 1),
        ),
    }
)


@pytest.mark.parametrize("reactions, expected", [(reactions_a, 31), (reactions_b, 165)])
def test_min_raw_material_required_to_make_chemical_product_is_properly_calculated(
    reactions, expected
):
    raw_material = "ORE"
    product = ChemicalQuantity("FUEL", 1)
    assert reactions.min_raw_material_to_make_product(raw_material, product) == expected
