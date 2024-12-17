from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

from .output_3_bit import HaltOutput3Bit
from .program_3_bit import Program3Bit, run_3_bit_program


@dataclass(frozen=True)
class _CandidateBatch:
    candidates: Iterable[int]
    bit_offset: int
    num_bits: int

    @property
    def total_bits(self) -> int:
        return self.bit_offset + self.num_bits

    def merge(self, other: "_CandidateBatch") -> "_CandidateBatch":
        # TODO: Refactor
        new_offset = min(self.bit_offset, other.bit_offset)
        new_num_bits = max(self.total_bits, other.total_bits) - new_offset
        new_candidates = set()
        for candidate_a in self.candidates:
            number_a = candidate_a << self.bit_offset
            for candidate_b in other.candidates:
                number_b = candidate_b << other.bit_offset
                aux = number_a ^ number_b
                aux >>= max(self.bit_offset, other.bit_offset)
                intersection_size = min(self.total_bits, other.total_bits) - max(
                    self.bit_offset, other.bit_offset
                )
                are_compatible = (aux % (1 << intersection_size)) == 0
                if are_compatible:
                    new_number = number_a | number_b
                    new_candidate = new_number >> new_offset
                    new_candidates.add(new_candidate)
        return _CandidateBatch(new_candidates, new_offset, new_num_bits)

    def smallest_candidate(self) -> int:
        return min(self.candidates) << self.bit_offset


class _CandidateBuilder:
    def __init__(self):
        self._batch = None

    def add_candidate_batch(self, candidate_batch: _CandidateBatch) -> None:
        if not self._batch:
            self._batch = candidate_batch
        else:
            self._batch = self._batch.merge(candidate_batch)

    def smallest_candidate(self) -> int:
        return self._batch.smallest_candidate()


def a_register_value_to_produce_quine(instructions: tuple[int, ...]) -> int:
    program = Program3Bit(instructions)
    output_map = defaultdict(set)
    halt_output = HaltOutput3Bit()
    for a in range(1024):
        registers = {"A": a, "B": 0, "C": 0}
        run_3_bit_program(program, halt_output, registers)
        output_map[halt_output.output_value].add(a)
    candidate_builder = _CandidateBuilder()
    bit_offset = 0
    for expected_output in instructions:
        candidate_batch = _CandidateBatch(
            candidates=output_map[expected_output], bit_offset=bit_offset, num_bits=10
        )
        candidate_builder.add_candidate_batch(candidate_batch)
        bit_offset += 3
    return candidate_builder.smallest_candidate()
