from .game_state import InfectionGameState


class InfectionGame:
    def __init__(self, initial_state: InfectionGameState) -> None:
        self._state = initial_state

    @property
    def state(self) -> InfectionGameState:
        return self._state

    def run_until_over(self) -> None:
        while not self._state.is_over:
            self._state = self._state.play_round()

    @property
    def immune_system_won(self) -> bool:
        return bool(self._state.immune_system_armies) and not bool(
            self._state.infection_armies
        )
