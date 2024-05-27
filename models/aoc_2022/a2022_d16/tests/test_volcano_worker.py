from ..logic import VolcanoWorker, Valve


def _build_valve(
    valve_id: chr = "A", flow_rate: int = 20, time_to_open: int = 1
) -> Valve:
    return Valve(valve_id, flow_rate, time_to_open)


def test_volcano_worker_changes_state_when_going_idle():
    valve = _build_valve()
    worker = VolcanoWorker(is_idle=False, valve=valve, task_completion_time=7)
    new_worker = worker.go_idle()
    assert new_worker == VolcanoWorker(
        is_idle=True, valve=valve, task_completion_time=7
    )


def test_volcano_worker_changes_state_when_they_start_opening_valve():
    valve_a = _build_valve()
    valve_b = _build_valve()
    worker = VolcanoWorker(is_idle=True, valve=valve_a, task_completion_time=7)
    new_worker = worker.start_opening_valve(task_completion_time=123, valve=valve_b)
    assert new_worker == VolcanoWorker(
        is_idle=False, valve=valve_b, task_completion_time=123
    )
