class PolymerExtension:
    def __init__(self, rules: dict[str, str]) -> None:
        self._rules = rules

    def extend(self, polymer: str) -> str:
        extended = ""
        for i in range(len(polymer) - 1):
            pair = polymer[i : i + 2]
            if pair in self._rules:
                extended += polymer[i] + self._rules[pair]
            else:
                extended += polymer[i]
        if len(polymer) > 0:
            extended += polymer[-1]
        return extended

    def extend_multiple_times(self, polymer: str, num_times: int) -> str:
        extended = polymer
        for _ in range(num_times):
            extended = self.extend(extended)
        return extended
