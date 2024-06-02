from models.common.cellular_automata import OneDimensionalBinaryCelullarAutomaton


class PlantAutomaton(OneDimensionalBinaryCelullarAutomaton):
    def __init__(
        self,
        rules: dict[tuple[int, ...], int],
        initial_state: set[int],
    ) -> None:
        super().__init__(rules)
        self._initial_state = initial_state

    def plants_alive(self, generation: int) -> set[int]:
        state = self._initial_state
        for _ in range(generation):
            state = self.next_state(state)
        return state
