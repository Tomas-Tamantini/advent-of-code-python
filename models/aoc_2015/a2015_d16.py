class AuntSue:
    def __init__(self, id: int, attributes: dict[str, int]) -> None:
        self._id = id
        self._attributes = attributes

    @property
    def id(self) -> int:
        return self._id

    def matches(self, other_attributes: dict[str, int]) -> bool:
        for attribute, value in self._attributes.items():
            if other_attributes[attribute] != value:
                return False
        return True
