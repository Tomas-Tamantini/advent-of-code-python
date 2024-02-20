from math import ceil
from dataclasses import dataclass
from collections import defaultdict
from models.graphs import topological_sorting


@dataclass(frozen=True)
class ChemicalQuantity:
    chemical: str
    quantity: int


@dataclass(frozen=True)
class ChemicalReaction:
    inputs: tuple[ChemicalQuantity, ...]
    output: ChemicalQuantity

    def inputs_required_to_produce_output(
        self, quantity: int
    ) -> tuple[ChemicalQuantity, ...]:
        multiplier = ceil(quantity / self.output.quantity)
        return tuple(
            ChemicalQuantity(chemical=inp.chemical, quantity=inp.quantity * multiplier)
            for inp in self.inputs
        )


class _ChemicalReactionsDag:
    def __init__(self, reactions: set[ChemicalReaction]) -> None:
        self._nodes = set()
        self._incoming = defaultdict(set)
        self._outgoing = defaultdict(set)

        for reaction in reactions:
            self._nodes.add(reaction.output.chemical)
            for inp in reaction.inputs:
                self._nodes.add(inp.chemical)
                self._outgoing[reaction.output.chemical].add(inp.chemical)
                self._incoming[inp.chemical].add(reaction.output.chemical)

    def nodes(self) -> set[str]:
        return self._nodes

    def incoming(self, node: str) -> set[str]:
        return self._incoming[node]

    def outgoing(self, node: str) -> set[str]:
        return self._outgoing[node]


class ChemicalReactions:
    def __init__(self, reactions: set[ChemicalReaction]):
        self._reactions = {reaction.output.chemical: reaction for reaction in reactions}
        self._dag = _ChemicalReactionsDag(reactions)

    def min_raw_material_to_make_product(
        self, raw_material: str, product: ChemicalQuantity
    ) -> int:
        required = defaultdict(int)
        required[product.chemical] = product.quantity
        for chemical in topological_sorting(self._dag):
            if chemical == raw_material:
                break
            reaction = self._reactions[chemical]
            quantity = required[chemical]
            required.pop(chemical)
            for inp in reaction.inputs_required_to_produce_output(quantity):
                required[inp.chemical] += inp.quantity
        return required[raw_material]
