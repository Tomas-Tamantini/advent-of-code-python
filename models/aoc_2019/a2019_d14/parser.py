from typing import Iterator
from models.common.io import InputReader
from .chemical_reactions import ChemicalQuantity, ChemicalReaction


def _parse_chemical_quantity(quantity_str: str) -> ChemicalQuantity:
    quantity, chemical = quantity_str.split()
    return ChemicalQuantity(chemical=chemical, quantity=int(quantity))


def _parse_chemical_reaction(reaction_str: str) -> ChemicalReaction:
    input_str, output_str = reaction_str.split(" => ")
    output = _parse_chemical_quantity(output_str)
    inputs = tuple(_parse_chemical_quantity(q) for q in input_str.split(", "))
    return ChemicalReaction(inputs, output)


def parse_chemical_reactions(input_reader: InputReader) -> Iterator[ChemicalReaction]:
    for line in input_reader.readlines():
        yield _parse_chemical_reaction(line.strip())
