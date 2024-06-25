from typing import Iterator
from models.common.io import IOHandler, Problem, ProblemSolution
from .parser import parse_chemical_reactions
from .chemical_reactions import ChemicalReactions, ChemicalQuantity


def aoc_2019_d14(io_handler: IOHandler) -> Iterator[ProblemSolution]:
    problem_id = Problem(2019, 14, "Space Stoichiometry")
    io_handler.output_writer.write_header(problem_id)
    reactions = ChemicalReactions(
        set(parse_chemical_reactions(io_handler.input_reader))
    )
    raw_material = "ORE"
    product = "FUEL"
    ore_required = reactions.min_raw_material_to_make_product(
        raw_material, product=ChemicalQuantity(product, quantity=1)
    )
    yield ProblemSolution(
        problem_id,
        f"Minimum ore required to make 1 fuel is {ore_required}",
        part=1,
        result=ore_required,
    )

    fuel_produced = reactions.max_product_that_can_be_produced(
        raw_material=ChemicalQuantity(raw_material, quantity=1_000_000_000_000),
        product=product,
    )
    yield ProblemSolution(
        problem_id,
        f"Maximum fuel that can be produced with 1 trillion ore is {fuel_produced}",
        part=2,
        result=fuel_produced,
    )
