from ..logic import ResourceType, ResourceQuantity


def test_resource_quantity_is_hashable():
    quantity_a = ResourceQuantity({ResourceType.ORE: 1, ResourceType.CLAY: 2})
    quantity_b = ResourceQuantity({ResourceType.ORE: 1, ResourceType.CLAY: 2})
    assert quantity_a == quantity_b
    assert hash(quantity_a) == hash(quantity_b)

    quantity_c = ResourceQuantity(
        {ResourceType.ORE: 1, ResourceType.CLAY: 2, ResourceType.OBSIDIAN: 3}
    )
    assert quantity_a != quantity_c
    assert hash(quantity_a) != hash(quantity_c)


def test_resource_quantity_is_leq_other_if_all_resoureces_are_leq():
    quantity_a = ResourceQuantity({ResourceType.ORE: 1, ResourceType.CLAY: 2})
    quantity_b = ResourceQuantity({ResourceType.ORE: 1, ResourceType.CLAY: 2})

    assert quantity_a.all_resources_leq(quantity_b)
    assert quantity_b.all_resources_leq(quantity_a)

    quantity_c = ResourceQuantity({ResourceType.ORE: 2, ResourceType.CLAY: 1})
    assert not quantity_a.all_resources_leq(quantity_c)
    assert not quantity_c.all_resources_leq(quantity_a)

    quantity_d = ResourceQuantity(
        {ResourceType.ORE: 2, ResourceType.CLAY: 2, ResourceType.OBSIDIAN: 3}
    )
    assert quantity_a.all_resources_leq(quantity_d)
    assert not quantity_d.all_resources_leq(quantity_a)


def test_resource_quantities_can_be_added():
    quantity_a = ResourceQuantity({ResourceType.ORE: 1, ResourceType.CLAY: 2})
    quantity_b = ResourceQuantity(
        {ResourceType.ORE: 3, ResourceType.CLAY: 1, ResourceType.OBSIDIAN: 5}
    )

    quantity_c = quantity_a + quantity_b
    assert quantity_c == ResourceQuantity(
        {ResourceType.ORE: 4, ResourceType.CLAY: 3, ResourceType.OBSIDIAN: 5}
    )


def test_resource_quantities_can_be_subtracted():
    quantity_a = ResourceQuantity({ResourceType.ORE: 1, ResourceType.CLAY: 2})
    quantity_b = ResourceQuantity(
        {ResourceType.ORE: 3, ResourceType.CLAY: 2, ResourceType.OBSIDIAN: 5}
    )

    quantity_c = quantity_b - quantity_a
    assert quantity_c == ResourceQuantity(
        {ResourceType.ORE: 2, ResourceType.OBSIDIAN: 5}
    )


def test_resource_quantities_can_be_incremented_by_one():
    quantity = ResourceQuantity({ResourceType.ORE: 1, ResourceType.CLAY: 2})
    new_quantity = quantity.increment_resource(ResourceType.ORE)
    assert new_quantity == ResourceQuantity({ResourceType.ORE: 2, ResourceType.CLAY: 2})
    new_quantity = new_quantity.increment_resource(ResourceType.GEODE)
    assert new_quantity == ResourceQuantity(
        {ResourceType.ORE: 2, ResourceType.CLAY: 2, ResourceType.GEODE: 1}
    )