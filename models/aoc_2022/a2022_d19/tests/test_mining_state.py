from ..logic import ResourceType, ResourceQuantity, Blueprint, MiningState


def _build_blueprint(costs: dict[ResourceType, ResourceQuantity] = None) -> Blueprint:
    costs = costs or dict()
    return Blueprint(blueprint_id=1, costs=costs)


def test_next_mining_state_increments_timestamp():
    state = MiningState(
        timestamp=123,
        inventory=ResourceQuantity(dict()),
        robots=ResourceQuantity(dict()),
    )
    new_states = set(state.next_states(blueprint=_build_blueprint()))
    assert len(new_states) == 1
    new_state = new_states.pop()
    assert new_state.timestamp == 124


def test_next_mining_state_increments_inventory_with_its_robots():
    state = MiningState(
        timestamp=0,
        inventory=ResourceQuantity({ResourceType.OBSIDIAN: 1, ResourceType.GEODE: 2}),
        robots=ResourceQuantity({ResourceType.ORE: 2, ResourceType.GEODE: 4}),
    )
    new_states = set(state.next_states(blueprint=_build_blueprint()))
    assert len(new_states) == 1
    new_state = new_states.pop()
    assert new_state.inventory == ResourceQuantity(
        {ResourceType.OBSIDIAN: 1, ResourceType.GEODE: 6, ResourceType.ORE: 2}
    )


def test_next_mining_states_contains_robots_that_were_built():
    state = MiningState(
        timestamp=0,
        inventory=ResourceQuantity({ResourceType.OBSIDIAN: 1, ResourceType.GEODE: 2}),
        robots=ResourceQuantity({ResourceType.ORE: 2, ResourceType.GEODE: 4}),
    )
    blueprint = _build_blueprint(
        {
            ResourceType.ORE: ResourceQuantity(
                {ResourceType.OBSIDIAN: 1, ResourceType.GEODE: 1}
            ),
            ResourceType.GEODE: ResourceQuantity(
                {ResourceType.OBSIDIAN: 12, ResourceType.GEODE: 3}
            ),
            ResourceType.OBSIDIAN: ResourceQuantity(
                {ResourceType.OBSIDIAN: 1, ResourceType.GEODE: 6, ResourceType.ORE: 2}
            ),
        }
    )
    new_states = set(state.next_states(blueprint))
    assert new_states == {
        MiningState(
            timestamp=1,
            inventory=ResourceQuantity(
                {ResourceType.OBSIDIAN: 1, ResourceType.GEODE: 6, ResourceType.ORE: 2}
            ),
            robots=ResourceQuantity({ResourceType.ORE: 2, ResourceType.GEODE: 4}),
        ),
        MiningState(
            timestamp=1,
            inventory=ResourceQuantity({ResourceType.GEODE: 5, ResourceType.ORE: 2}),
            robots=ResourceQuantity({ResourceType.ORE: 3, ResourceType.GEODE: 4}),
        ),
        MiningState(
            timestamp=1,
            inventory=ResourceQuantity(dict()),
            robots=ResourceQuantity(
                {ResourceType.ORE: 2, ResourceType.GEODE: 4, ResourceType.OBSIDIAN: 1}
            ),
        ),
    }
