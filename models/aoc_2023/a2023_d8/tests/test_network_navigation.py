import pytest

from ..logic import BinaryNetwork, NetworkStep

_CONNECTIONS_1 = {
    "AAA": ("BBB", "CCC"),
    "BBB": ("DDD", "EEE"),
    "CCC": ("ZZZ", "GGG"),
    "DDD": ("DDD", "DDD"),
    "EEE": ("EEE", "EEE"),
    "GGG": ("GGG", "GGG"),
    "ZZZ": ("ZZZ", "ZZZ"),
}

_CONNECTIONS_2 = {
    "AAA": ("BBB", "BBB"),
    "BBB": ("AAA", "ZZZ"),
    "ZZZ": ("ZZZ", "ZZZ"),
}

_CONNECTIONS_3 = {
    "11A": ("11B", "XXX"),
    "11B": ("XXX", "11Z"),
    "11Z": ("11B", "XXX"),
    "22A": ("22B", "XXX"),
    "22B": ("22C", "22C"),
    "22C": ("22Z", "22Z"),
    "22Z": ("22B", "22B"),
    "XXX": ("XXX", "XXX"),
}

_STEPS_RL = [NetworkStep.RIGHT, NetworkStep.LEFT]
_STEPS_LLR = [NetworkStep.LEFT, NetworkStep.LEFT, NetworkStep.RIGHT]


@pytest.mark.parametrize(
    ("steps", "connections", "expected_num_steps"),
    [
        (_STEPS_RL, _CONNECTIONS_1, 2),
        (_STEPS_LLR, _CONNECTIONS_2, 6),
    ],
)
def test_network_navigation_finds_how_many_steps_single_traveler_takes_to_complete(
    steps, connections, expected_num_steps
):
    steps = _STEPS_RL
    connections = _CONNECTIONS_1
    expected_num_steps = 2
    network = BinaryNetwork(connections, steps)
    num_steps = network.num_steps_to_finish(start_nodes=["AAA"], end_nodes=["ZZZ"])
    assert expected_num_steps == num_steps


def test_network_navigation_finds_how_many_steps_multiple_traveler_take_to_complete_simultaneously():
    steps = [NetworkStep.LEFT, NetworkStep.RIGHT]
    network = BinaryNetwork(_CONNECTIONS_3, steps)
    num_steps = network.num_steps_to_finish(
        start_nodes=["11A", "22A"], end_nodes=["11Z", "22Z"]
    )
    assert 6 == num_steps
