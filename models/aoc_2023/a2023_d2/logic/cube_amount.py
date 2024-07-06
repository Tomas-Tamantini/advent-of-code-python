from dataclasses import dataclass


@dataclass(frozen=True)
class CubeAmount:
    amount_by_color: dict[str, int]

    def _amount_for_color(self, color: str) -> int:
        return self.amount_by_color.get(color, 0)

    def all_colors_leq(self, other: "CubeAmount") -> bool:
        return all(
            amount <= other._amount_for_color(color)
            for color, amount in self.amount_by_color.items()
        )

    @staticmethod
    def merge(*amounts: "CubeAmount") -> "CubeAmount":
        colors = set().union(*(amount.amount_by_color for amount in amounts))
        return CubeAmount(
            {
                color: max(amount._amount_for_color(color) for amount in amounts)
                for color in colors
            }
        )
