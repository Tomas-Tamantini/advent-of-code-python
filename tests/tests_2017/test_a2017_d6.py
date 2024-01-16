from models.aoc_2017 import MemoryBankBalancer


def test_balancer_iterates_through_configurations_following_the_rules():
    initial_config = [0, 2, 7, 0]
    balancer = MemoryBankBalancer(initial_config)
    assert list(balancer.unique_configurations()) == [
        (0, 2, 7, 0),
        (2, 4, 1, 2),
        (3, 1, 2, 3),
        (0, 2, 3, 4),
        (1, 3, 4, 1),
        (2, 4, 1, 2),
    ]
