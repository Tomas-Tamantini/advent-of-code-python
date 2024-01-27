from .binary_automata import OneDimensionalBinaryCelullarAutomaton


class ElementaryAutomaton(OneDimensionalBinaryCelullarAutomaton):
    def __init__(self, rule: int) -> None:
        if not 0 <= rule < 256:
            raise ValueError("Rule index must be between 0 and 255")
        rule_binary = f"{rule:08b}"
        rules = {
            (1, 1, 1): int(rule_binary[0]),
            (1, 1, 0): int(rule_binary[1]),
            (1, 0, 1): int(rule_binary[2]),
            (1, 0, 0): int(rule_binary[3]),
            (0, 1, 1): int(rule_binary[4]),
            (0, 1, 0): int(rule_binary[5]),
            (0, 0, 1): int(rule_binary[6]),
            (0, 0, 0): int(rule_binary[7]),
        }
        super().__init__(rules)
