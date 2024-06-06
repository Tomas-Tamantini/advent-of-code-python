from .resource_type import ResourceType


class ResourceQuantity:
    def __init__(self, quantity: dict[ResourceType, int]) -> None:
        self._quantity = quantity

    def resource_amount(self, resource: ResourceType) -> int:
        return self._quantity.get(resource, 0)

    def all_resources_leq(self, other: "ResourceQuantity") -> bool:
        for resource, amount in self._quantity.items():
            if other.resource_amount(resource) < amount:
                return False
        return True

    def increment_resource(self, resource: ResourceType) -> "ResourceQuantity":
        new_quantity = self._quantity.copy()
        new_quantity[resource] = self.resource_amount(resource) + 1
        return ResourceQuantity(new_quantity)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResourceQuantity):
            return NotImplemented
        return self._quantity == other._quantity

    def __hash__(self) -> int:
        return hash(frozenset(self._quantity.items()))

    def __add__(self, other: "ResourceQuantity") -> "ResourceQuantity":
        new_quantity = self._quantity.copy()
        for resource, amount in other._quantity.items():
            new_quantity[resource] = self.resource_amount(resource) + amount
        return ResourceQuantity(new_quantity)

    def __sub__(self, other: "ResourceQuantity") -> "ResourceQuantity":
        new_quantity = self._quantity.copy()
        for resource, amount in other._quantity.items():
            new_quantity[resource] = self.resource_amount(resource) - amount
            if new_quantity[resource] == 0:
                del new_quantity[resource]
        return ResourceQuantity(new_quantity)
