from dataclasses import dataclass
from typing import Iterator
from models.common.graphs import DirectedGraph
from .valve import Valve

TIME_TO_OPEN_VALVE = 1
TIME_TO_TRAVEL_BETWEEN_VALVES = 1


@dataclass(frozen=True)
class ValvesState:
    current_valve: Valve
    open_valves: set[Valve]
    time_elapsed: int
    pressure_released: int

    @staticmethod
    def _pressure_increase(open_valves: set[Valve], time_interval: int) -> int:
        return sum(time_interval * open_valve.flow_rate for open_valve in open_valves)

    def pressure_release_upper_bound(
        self, total_time: int, all_valves: set[Valve]
    ) -> int:
        upper_bound = self.pressure_released
        time_left = total_time - self.time_elapsed
        if time_left <= 0:
            return upper_bound
        extended_open = self.open_valves | {self.current_valve}
        upper_bound += self._pressure_increase(extended_open, time_left)
        remaining_valves = all_valves - extended_open
        for next_valve_to_open in sorted(remaining_valves, key=lambda v: -v.flow_rate):
            time_left -= TIME_TO_TRAVEL_BETWEEN_VALVES + TIME_TO_OPEN_VALVE
            if time_left <= 0:
                return upper_bound
            upper_bound += time_left * next_valve_to_open.flow_rate
        return upper_bound

    def next_states(
        self, total_time: int, valves_graph: DirectedGraph
    ) -> Iterator["ValvesState"]:
        if (
            self.current_valve not in self.open_valves
            and self.current_valve.flow_rate > 0
            and self.time_elapsed + TIME_TO_OPEN_VALVE <= total_time
        ):
            yield ValvesState(
                current_valve=self.current_valve,
                open_valves=self.open_valves | {self.current_valve},
                time_elapsed=self.time_elapsed + TIME_TO_OPEN_VALVE,
                pressure_released=self.pressure_released
                + self._pressure_increase(self.open_valves, TIME_TO_OPEN_VALVE),
            )
        if self.time_elapsed + TIME_TO_TRAVEL_BETWEEN_VALVES <= total_time:
            for neighboring_valve in valves_graph.neighbors(self.current_valve):
                yield ValvesState(
                    current_valve=neighboring_valve,
                    open_valves=self.open_valves,
                    time_elapsed=self.time_elapsed + TIME_TO_TRAVEL_BETWEEN_VALVES,
                    pressure_released=self.pressure_released
                    + self._pressure_increase(
                        self.open_valves, TIME_TO_TRAVEL_BETWEEN_VALVES
                    ),
                )
