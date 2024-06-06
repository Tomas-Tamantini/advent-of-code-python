from .resource_type import ResourceType


class ResourceQuantity:
    def __init__(self, quantity: dict[ResourceType, int]) -> None:
        self._quantity = quantity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResourceQuantity):
            return NotImplemented
        return self._quantity == other._quantity

    def __hash__(self) -> int:
        return hash(frozenset(self._quantity.items()))

    def all_resources_leq(self, other: "ResourceQuantity") -> bool:
        for resource, amount in self._quantity.items():
            if other._quantity.get(resource, 0) < amount:
                return False
        return True

    def __add__(self, other: "ResourceQuantity") -> "ResourceQuantity":
        new_quantity = self._quantity.copy()
        for resource, amount in other._quantity.items():
            new_quantity[resource] = new_quantity.get(resource, 0) + amount
        return ResourceQuantity(new_quantity)
