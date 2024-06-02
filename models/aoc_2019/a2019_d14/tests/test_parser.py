from models.common.io import InputFromString
from ..parser import parse_chemical_reactions
from ..chemical_reactions import ChemicalQuantity, ChemicalReaction


def test_parse_chemical_reactions():
    file_content = """2 MPHSH, 3 NQNX => 3 FWHL
                      144 ORE => 1 CXRVG"""
    reactions = list(parse_chemical_reactions(InputFromString(file_content)))
    assert reactions == [
        ChemicalReaction(
            inputs=(ChemicalQuantity("MPHSH", 2), ChemicalQuantity("NQNX", 3)),
            output=ChemicalQuantity("FWHL", 3),
        ),
        ChemicalReaction(
            inputs=(ChemicalQuantity("ORE", 144),), output=ChemicalQuantity("CXRVG", 1)
        ),
    ]
