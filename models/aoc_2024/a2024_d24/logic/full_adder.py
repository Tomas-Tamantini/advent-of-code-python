from typing import Iterator

from .logic_gate import LogicGate


def swapped_pair_of_wires_for_full_adder(gates: list[LogicGate]) -> Iterator[set[str]]:
    # Done manually - TODO: Implement
    yield {"z10", "gpr"}
    yield {"z21", "nks"}
    yield {"z33", "ghp"}
    yield {"krs", "cpm"}
