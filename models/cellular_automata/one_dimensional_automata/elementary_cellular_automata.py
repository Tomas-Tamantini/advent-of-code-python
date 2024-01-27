class ElementaryAutomaton:
    def __init__(self, rule: int) -> None:
        if not 0 <= rule < 256:
            raise ValueError("Rule index must be between 0 and 255")
        self._rule: dict[str, str] = self._generate_rule(rule)

    def _generate_rule(self, rule: int) -> dict[str, str]:
        rule_binary = f"{rule:08b}"
        return {
            "111": rule_binary[0],
            "110": rule_binary[1],
            "101": rule_binary[2],
            "100": rule_binary[3],
            "011": rule_binary[4],
            "010": rule_binary[5],
            "001": rule_binary[6],
            "000": rule_binary[7],
        }

    @staticmethod
    def _get_cell_neighborhood(cells: str, i: int) -> str:
        cell_left = cells[i - 1] if i > 0 else "0"
        cell_center = cells[i]
        cell_right = cells[i + 1] if i < len(cells) - 1 else "0"
        return f"{cell_left}{cell_center}{cell_right}"

    def next_state(self, cells: str) -> str:
        return "".join(
            self._rule[self._get_cell_neighborhood(cells, i)] for i in range(len(cells))
        )
