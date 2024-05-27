from unittest.mock import Mock
from ..logic import VolcanoState, VolcanoWorker, Valve


def _build_valve(
    valve_id: chr = "A", flow_rate: int = 20, time_to_open: int = 1
) -> Valve:
    return Valve(valve_id, flow_rate, time_to_open)


def _build_worker(
    is_idle: bool = True,
    valve: Valve = None,
    task_completion_time: int = 0,
) -> VolcanoWorker:
    valve = valve or _build_valve()
    return VolcanoWorker(is_idle, valve, task_completion_time)


def _build_state(
    elapsed_time: int = 0,
    pressure_released: int = 0,
    open_valves: set[Valve] = None,
    workers: tuple[VolcanoWorker, ...] = None,
) -> VolcanoState:
    if not workers:
        workers = (_build_worker(),)
    open_valves = open_valves or set()
    return VolcanoState(elapsed_time, pressure_released, open_valves, workers)


def _mock_volcano(
    time_until_eruption: int = 30,
    min_travel_time: int = 1,
    min_time_to_open_valve: int = 1,
    distance: int = 1,
    all_valves: set[Valve] = None,
):
    all_valves = all_valves or set()
    volcano = Mock()
    volcano.time_until_eruption = time_until_eruption
    volcano.min_travel_time = min_travel_time
    volcano.min_time_to_open_valve = min_time_to_open_valve
    volcano.distance.return_value = distance
    volcano.all_valves.return_value = all_valves
    return volcano


def test_volcano_has_no_next_state_if_time_is_up_for_eruption():
    state = _build_state(elapsed_time=30)
    volcano = _mock_volcano(time_until_eruption=30)
    assert list(state.next_states(volcano=volcano)) == []


def test_volcano_worker_starts_opening_closed_valve_if_they_are_idle():
    valve = _build_valve()
    worker = _build_worker(is_idle=True, valve=valve)
    state = _build_state(elapsed_time=0, workers=(worker,))
    volcano = _mock_volcano(all_valves={valve}, distance=0)
    next_states = list(state.next_states(volcano=volcano))
    assert len(next_states) == 1
    assert next_states[0].elapsed_time == 0
    assert next_states[0].workers[0] == _build_worker(
        is_idle=False, valve=valve, task_completion_time=1
    )


def test_volcano_worker_moves_to_different_valve_if_they_are_idle():
    valve_a = _build_valve("A")
    valve_b = _build_valve("B")
    worker = _build_worker(is_idle=True, valve=valve_a)
    state = _build_state(elapsed_time=0, workers=(worker,), open_valves={valve_a})
    volcano = _mock_volcano(distance=5, all_valves={valve_a, valve_b})
    next_states = list(state.next_states(volcano=volcano))
    assert len(next_states) == 1
    assert next_states[0].elapsed_time == 0
    assert next_states[0].workers[0] == _build_worker(
        is_idle=False, valve=valve_b, task_completion_time=6
    )


def test_volcano_worker_in_the_middle_of_task_completes_that_task():
    valve = _build_valve()
    worker = VolcanoWorker(is_idle=False, valve=valve, task_completion_time=12)
    state = _build_state(
        elapsed_time=0,
        pressure_released=100,
        open_valves={_build_valve(flow_rate=10)},
        workers=(worker,),
    )
    volcano = _mock_volcano()
    next_states = list(state.next_states(volcano=volcano))
    assert len(next_states) == 1
    assert next_states[0].elapsed_time == 12
    assert next_states[0].pressure_released == 220
    assert next_states[0].workers[0] == VolcanoWorker(
        is_idle=True, valve=valve, task_completion_time=12
    )


def test_volcano_skips_to_eruption_if_all_available_tasks_take_too_long():
    worker = _build_worker(
        is_idle=False, valve=_build_valve(), task_completion_time=1000
    )
    state = _build_state(elapsed_time=0, workers=(worker,))
    volcano = _mock_volcano(time_until_eruption=10)
    next_states = list(state.next_states(volcano=volcano))
    assert len(next_states) == 1
    assert next_states[0].elapsed_time == 10


def test_pressure_release_upper_bound_uses_minimum_time_to_travel_between_valves_and_open_them():
    volcano = _mock_volcano(
        min_travel_time=1,
        min_time_to_open_valve=1,
        time_until_eruption=30,
        all_valves={
            _build_valve("A", 10),
            _build_valve("B", 3),
            _build_valve("C", 32),
            _build_valve("D", 15),
            _build_valve("E", 20),
            _build_valve("F", 17),
            _build_valve("G", 8),
            _build_valve("H", 12),
            _build_valve("I", 0),
        },
    )
    state = _build_state(
        elapsed_time=25,
        pressure_released=13,
        workers=(_build_worker(valve=_build_valve("A", 10)),),
        open_valves={
            _build_valve("B", 3),
            _build_valve("C", 32),
        },
    )
    assert state.pressure_release_upper_bound(volcano=volcano) == 315


def test_pressure_release_upper_bound_increases_if_more_than_one_worker():
    volcano = _mock_volcano(
        min_travel_time=1,
        min_time_to_open_valve=1,
        all_valves={
            _build_valve("A", 10),
            _build_valve("B", 3),
            _build_valve("C", 32),
            _build_valve("D", 15),
            _build_valve("E", 20),
            _build_valve("F", 17),
            _build_valve("G", 8),
            _build_valve("H", 12),
            _build_valve("I", 0),
        },
    )
    state = _build_state(
        elapsed_time=25,
        pressure_released=13,
        workers=(
            _build_worker(valve=_build_valve("A", 10)),
            _build_worker(valve=_build_valve("H", 12)),
        ),
        open_valves={
            _build_valve("B", 3),
            _build_valve("C", 32),
        },
    )
    assert state.pressure_release_upper_bound(volcano=volcano) == 432
