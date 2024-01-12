from dataclasses import dataclass
from typing import Iterator, Optional
from itertools import combinations
from models.graphs import min_path_length_with_bfs


@dataclass(frozen=True)
class _FacilityItem:
    item_id: str
    is_generator: bool

    def __lt__(self, __value: object) -> bool:
        if not isinstance(__value, _FacilityItem):
            return NotImplemented
        return (self.item_id, self.is_generator) < (
            __value.item_id,
            __value.is_generator,
        )


@dataclass(frozen=True)
class FloorConfiguration:
    microchips: tuple[str, ...]
    generators: tuple[str, ...]

    @property
    def is_empty(self) -> bool:
        return not self.microchips and not self.generators

    def is_valid(self) -> bool:
        if not self.generators:
            return True
        return all(chip in self.generators for chip in self.microchips)

    def all_items(self) -> Iterator[_FacilityItem]:
        for item_id in self.microchips:
            yield _FacilityItem(item_id, is_generator=False)
        for item_id in self.generators:
            yield _FacilityItem(item_id, is_generator=True)

    def all_items_groupings(
        self, group_size: int
    ) -> Iterator[tuple[_FacilityItem, ...]]:
        return combinations(self.all_items(), group_size)

    def remove_item(self, item: _FacilityItem) -> "FloorConfiguration":
        if item.is_generator:
            return FloorConfiguration(
                microchips=self.microchips,
                generators=tuple(g for g in self.generators if g != item.item_id),
            )
        else:
            return FloorConfiguration(
                microchips=tuple(c for c in self.microchips if c != item.item_id),
                generators=self.generators,
            )

    def remove_items(self, *items: _FacilityItem) -> "FloorConfiguration":
        chips_to_remove = {i.item_id for i in items if not i.is_generator}
        generators_to_remove = {i.item_id for i in items if i.is_generator}
        return FloorConfiguration(
            microchips=tuple(c for c in self.microchips if c not in chips_to_remove),
            generators=tuple(
                g for g in self.generators if g not in generators_to_remove
            ),
        )

    def add_item(self, item: _FacilityItem) -> "FloorConfiguration":
        if item.is_generator:
            return FloorConfiguration(
                microchips=self.microchips,
                generators=self.generators + (item.item_id,),
            )
        else:
            return FloorConfiguration(
                microchips=self.microchips + (item.item_id,),
                generators=self.generators,
            )

    def add_items(self, *items: _FacilityItem) -> "FloorConfiguration":
        return FloorConfiguration(
            microchips=self.microchips
            + tuple(i.item_id for i in items if not i.is_generator),
            generators=self.generators
            + tuple(i.item_id for i in items if i.is_generator),
        )

    def _sorted_items(self) -> tuple[_FacilityItem, ...]:
        return tuple(sorted(self.all_items()))

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, FloorConfiguration):
            return NotImplemented
        return self._sorted_items() == __value._sorted_items()

    def __hash__(self) -> int:
        return hash(self._sorted_items())

    def __str__(self) -> str:
        microchips_repr = sorted([f"{c}m" for c in self.microchips])
        generators_repr = sorted([f"{g}g" for g in self.generators])
        return ".".join(microchips_repr + generators_repr)


@dataclass(frozen=True)
class RadioisotopeTestingFacility:
    floors: tuple[FloorConfiguration, ...]
    elevator_floor: int = 0

    def is_valid(self) -> bool:
        return all(floor.is_valid() for floor in self.floors)

    @property
    def _current_floor(self) -> FloorConfiguration:
        return self.floors[self.elevator_floor]

    def _try_move_up(self, *items: _FacilityItem) -> Optional[FloorConfiguration]:
        if self.elevator_floor >= len(self.floors) - 1:
            return None
        upper_floor = self.floors[self.elevator_floor + 1].add_items(*items)
        if upper_floor.is_valid():
            return upper_floor

    def _try_move_down(self, *items: _FacilityItem) -> Optional[FloorConfiguration]:
        if self.elevator_floor <= 0:
            return None
        lower_floor = self.floors[self.elevator_floor - 1].add_items(*items)
        if lower_floor.is_valid():
            return lower_floor

    def _move_up(
        self,
        future_current_floor: FloorConfiguration,
        future_upper_floor: FloorConfiguration,
    ) -> "RadioisotopeTestingFacility":
        return RadioisotopeTestingFacility(
            floors=(
                *self.floors[: self.elevator_floor],
                future_current_floor,
                future_upper_floor,
                *self.floors[self.elevator_floor + 2 :],
            ),
            elevator_floor=self.elevator_floor + 1,
        )

    def _move_down(
        self,
        future_current_floor: FloorConfiguration,
        future_lower_floor: FloorConfiguration,
    ) -> "RadioisotopeTestingFacility":
        return RadioisotopeTestingFacility(
            floors=(
                *self.floors[: self.elevator_floor - 1],
                future_lower_floor,
                future_current_floor,
                *self.floors[self.elevator_floor + 1 :],
            ),
            elevator_floor=self.elevator_floor - 1,
        )

    def _neighboring_valid_states_moving_n_items(
        self, num_items_to_move: int
    ) -> Iterator["RadioisotopeTestingFacility"]:
        for items in self._current_floor.all_items_groupings(
            group_size=num_items_to_move
        ):
            future_current_floor = self._current_floor.remove_items(*items)
            if not future_current_floor.is_valid():
                continue
            future_lower_floor = self._try_move_down(*items)
            if future_lower_floor is not None:
                yield self._move_down(future_current_floor, future_lower_floor)
            future_upper_floor = self._try_move_up(*items)
            if future_upper_floor is not None:
                yield self._move_up(future_current_floor, future_upper_floor)

    def neighboring_valid_states(self) -> Iterator["RadioisotopeTestingFacility"]:
        yield from self._neighboring_valid_states_moving_n_items(num_items_to_move=1)
        yield from self._neighboring_valid_states_moving_n_items(num_items_to_move=2)

    def is_final_state(self) -> bool:
        return all(floor.is_empty for floor in self.floors[:-1])

    def __str__(self) -> str:
        max_len = max(len(str(f)) for f in self.floors)

        def pad(s: str) -> str:
            return s + "." * (max_len - len(s))

        padded_floors = []
        for i, f in enumerate(self.floors):
            prefix = "E." if i == self.elevator_floor else ".."
            padded_floors.append(prefix + pad(str(f)))

        return "\n".join(reversed(padded_floors))

    def min_num_steps_to_reach_final_state(self) -> int:
        return min_path_length_with_bfs(self)
