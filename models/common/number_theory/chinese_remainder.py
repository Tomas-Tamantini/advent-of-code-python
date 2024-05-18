from dataclasses import dataclass
from .gcd_and_lcm import are_coprime


@dataclass
class ChineseRemainder:
    divisor: int
    remainder: int

    def combine(self, other: "ChineseRemainder") -> "ChineseRemainder":
        if not are_coprime(self.divisor, other.divisor):
            raise NotImplementedError("Cannot combine non-coprime remainders")
        new_divisor = self.divisor * other.divisor
        for guess in range(self.remainder, new_divisor, self.divisor):
            if guess % other.divisor == other.remainder:
                return ChineseRemainder(divisor=new_divisor, remainder=guess)


def solve_chinese_remainder_system(*remainders: ChineseRemainder) -> int:
    combined_remainder = remainders[0]
    for remainder in remainders[1:]:
        combined_remainder = combined_remainder.combine(remainder)
    return combined_remainder.remainder
