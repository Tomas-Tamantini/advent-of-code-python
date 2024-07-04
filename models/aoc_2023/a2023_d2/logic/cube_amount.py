from dataclasses import dataclass


@dataclass(frozen=True)
class CubeAmount:
    amount_by_color: dict[str, int]

    def all_colors_leq(self, other: "CubeAmount") -> bool:
        return all(
            amount <= other.amount_by_color.get(color, 0)
            for color, amount in self.amount_by_color.items()
        )
