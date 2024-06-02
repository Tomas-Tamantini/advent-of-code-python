import pytest
from ..chemical_reactions import ChemicalQuantity, ChemicalReaction, ChemicalReactions


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


example_reactions = [
    ChemicalReactions(
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
    ),
    ChemicalReactions(
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
    ),
    ChemicalReactions(
        {
            ChemicalReaction(
                inputs=(ChemicalQuantity("ORE", 157),),
                output=ChemicalQuantity("NZVS", 5),
            ),
            ChemicalReaction(
                inputs=(ChemicalQuantity("ORE", 165),),
                output=ChemicalQuantity("DCFZ", 6),
            ),
            ChemicalReaction(
                inputs=(
                    ChemicalQuantity("XJWVT", 44),
                    ChemicalQuantity("KHKGT", 5),
                    ChemicalQuantity("QDVJ", 1),
                    ChemicalQuantity("NZVS", 29),
                    ChemicalQuantity("GPVTF", 9),
                    ChemicalQuantity("HKGWZ", 48),
                ),
                output=ChemicalQuantity("FUEL", 1),
            ),
            ChemicalReaction(
                inputs=(
                    ChemicalQuantity("HKGWZ", 12),
                    ChemicalQuantity("GPVTF", 1),
                    ChemicalQuantity("PSHF", 8),
                ),
                output=ChemicalQuantity("QDVJ", 9),
            ),
            ChemicalReaction(
                inputs=(ChemicalQuantity("ORE", 179),),
                output=ChemicalQuantity("PSHF", 7),
            ),
            ChemicalReaction(
                inputs=(ChemicalQuantity("ORE", 177),),
                output=ChemicalQuantity("HKGWZ", 5),
            ),
            ChemicalReaction(
                inputs=(
                    ChemicalQuantity("DCFZ", 7),
                    ChemicalQuantity("PSHF", 7),
                ),
                output=ChemicalQuantity("XJWVT", 2),
            ),
            ChemicalReaction(
                inputs=(ChemicalQuantity("ORE", 165),),
                output=ChemicalQuantity("GPVTF", 2),
            ),
            ChemicalReaction(
                inputs=(
                    ChemicalQuantity("DCFZ", 3),
                    ChemicalQuantity("NZVS", 7),
                    ChemicalQuantity("HKGWZ", 5),
                    ChemicalQuantity("PSHF", 10),
                ),
                output=ChemicalQuantity("KHKGT", 8),
            ),
        }
    ),
]


@pytest.mark.parametrize(
    "reactions, expected",
    [
        (example_reactions[0], 31),
        (example_reactions[1], 165),
        (example_reactions[2], 13312),
    ],
)
def test_min_raw_material_required_to_make_chemical_product_is_properly_calculated(
    reactions, expected
):
    raw_material = "ORE"
    product = ChemicalQuantity("FUEL", 1)
    assert reactions.min_raw_material_to_make_product(raw_material, product) == expected


def test_max_product_that_can_be_produced_given_amount_of_raw_material_is_properly_calculated():
    reactions = example_reactions[2]
    raw_material = ChemicalQuantity("ORE", 1_000_000_000_000)
    product = "FUEL"
    assert (
        reactions.max_product_that_can_be_produced(raw_material, product) == 82_892_753
    )
