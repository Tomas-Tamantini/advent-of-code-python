from models.common.graphs import DirectedGraph

from ..jobshop import time_to_complete_jobs


def test_if_no_jobs_time_to_complete_is_zero():
    empty_dag = DirectedGraph()
    assert (
        time_to_complete_jobs(num_workers=1, jobs_dag=empty_dag, job_durations={}) == 0
    )


def test_if_single_worker_time_to_complete_jobs_is_simple_sum():
    jobs_dag = DirectedGraph()
    jobs_dag.add_node("A")
    jobs_dag.add_node("B")
    times = {"A": 1, "B": 2}
    assert (
        time_to_complete_jobs(num_workers=1, jobs_dag=jobs_dag, job_durations=times)
        == 3
    )


def test_workers_do_jobs_in_parallel():
    jobs_dag = DirectedGraph()
    jobs_dag.add_node("A")
    jobs_dag.add_node("B")
    times = {"A": 1, "B": 2}
    assert (
        time_to_complete_jobs(num_workers=2, jobs_dag=jobs_dag, job_durations=times)
        == 2
    )


def test_jobs_must_obey_precedence_order():
    jobs_dag = DirectedGraph()
    jobs_dag.add_edge("A", "B")
    times = {"A": 1, "B": 2}
    assert (
        time_to_complete_jobs(num_workers=2, jobs_dag=jobs_dag, job_durations=times)
        == 3
    )


def test_if_multiple_jobs_are_free_tie_breaker_is_alphabetical_order():
    jobs_dag = DirectedGraph()
    jobs_dag.add_edge("C", "A")
    jobs_dag.add_edge("C", "F")
    jobs_dag.add_edge("A", "B")
    jobs_dag.add_edge("A", "D")
    jobs_dag.add_edge("B", "E")
    jobs_dag.add_edge("D", "E")
    jobs_dag.add_edge("F", "E")
    times = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
    assert (
        time_to_complete_jobs(num_workers=2, jobs_dag=jobs_dag, job_durations=times)
        == 15
    )
