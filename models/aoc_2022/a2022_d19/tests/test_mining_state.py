from ..logic import MiningState, ResourceType


def test_mining_state_stores_inventory():
    inventory = {ResourceType.ORE: 1, ResourceType.CLAY: 2}
    state = MiningState(inventory=inventory, fleet_size={})
    assert state.resource_amount(ResourceType.CLAY) == 2
    assert state.resource_amount(ResourceType.GEODE) == 0


def test_mining_state_stores_fleet_size():
    fleet_size = {ResourceType.ORE: 1, ResourceType.CLAY: 2}
    state = MiningState(inventory={}, fleet_size=fleet_size)
    assert state.num_robots(ResourceType.CLAY) == 2
    assert state.num_robots(ResourceType.GEODE) == 0
