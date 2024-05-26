from ..logic import VolcanoWorker, WorkerState, Valve


def _build_valve(
    valve_id: chr = "A", flow_rate: int = 20, time_to_open: int = 1
) -> Valve:
    return Valve(valve_id, flow_rate, time_to_open)


def test_volcano_worker_changes_state_when_going_idle():
    valve = _build_valve()
    worker = VolcanoWorker(
        state=WorkerState.EN_ROUTE, valve=valve, task_completion_time=7
    )
    new_worker = worker.go_idle()
    assert new_worker == VolcanoWorker(
        state=WorkerState.IDLE, valve=valve, task_completion_time=7
    )


def test_volcano_worker_changes_state_when_waiting_for_eruption():
    valve = _build_valve()
    worker = VolcanoWorker(state=WorkerState.IDLE, valve=valve, task_completion_time=7)
    new_worker = worker.wait_for_eruption(task_completion_time=123)
    assert new_worker == VolcanoWorker(
        state=WorkerState.WAITING_FOR_ERUPTION, valve=valve, task_completion_time=123
    )


def test_volcano_worker_changes_state_when_they_start_opening_valve():
    valve = _build_valve()
    worker = VolcanoWorker(state=WorkerState.IDLE, valve=valve, task_completion_time=7)
    new_worker = worker.start_opening_valve(task_completion_time=123)
    assert new_worker == VolcanoWorker(
        state=WorkerState.OPENING_VALVE, valve=valve, task_completion_time=123
    )


def test_volcano_worker_changes_state_and_valve_when_they_start_to_move_towards_new_valve():
    valve_a = _build_valve("A")
    valve_b = _build_valve("B")
    worker = VolcanoWorker(
        state=WorkerState.IDLE, valve=valve_a, task_completion_time=7
    )
    new_worker = worker.start_moving_towards(valve_b, task_completion_time=123)
    assert new_worker == VolcanoWorker(
        state=WorkerState.EN_ROUTE, valve=valve_b, task_completion_time=123
    )
