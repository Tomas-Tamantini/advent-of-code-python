from .bot_moves import CaveGameBot
from .cave_map import CaveMap
from .game_state import CaveGameState


class CaveGame:
    def __init__(self, cave_map: CaveMap, initial_units: CaveGameState) -> None:
        self._map = cave_map
        if initial_units.has_duplicate_ids():
            raise ValueError("Duplicate unit ids")
        self._state = initial_units
        self._round = 0
        self._initial_num_elves = len(self._state.elves)
        self._initial_num_goblins = len(self._state.goblins)

    @property
    def cave_map(self) -> CaveMap:
        return self._map

    @property
    def elf_casualties(self) -> int:
        return self._initial_num_elves - len(self._state.elves)

    @property
    def goblin_casualties(self) -> int:
        return self._initial_num_goblins - len(self._state.goblins)

    @property
    def state(self) -> CaveGameState:
        return self._state

    @property
    def round(self) -> int:
        return self._round

    def play_until_over(self, bot: CaveGameBot) -> None:
        while not self._state.game_is_over():
            self.play_round(bot)

    def play_round(self, bot: CaveGameBot) -> None:
        sorted_units_ids = [
            unit.unit_id for unit in self._state.units_in_reading_order()
        ]
        for unit_id in sorted_units_ids:
            if self._state.game_is_over():
                return
            try:
                unit = self._state.get_unit_from_id(unit_id)
            except ValueError:
                continue
            for move in bot.bot_moves(unit, self._state, self._map):
                self._state = move.execute(unit, self._state)
        self._round += 1
