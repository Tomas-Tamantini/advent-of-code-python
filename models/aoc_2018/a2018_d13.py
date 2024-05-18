from typing import Iterator, Optional
from models.common.vectors import Vector2D, CardinalDirection, TurnDirection


class _MineCart:
    def __init__(
        self,
        id: int,
        position: Vector2D,
        direction: CardinalDirection,
        intersection_sequence: list[TurnDirection],
    ) -> None:
        self._id = id
        self._position = position
        self._direction = direction
        self._intersection_sequence = intersection_sequence
        self._current_intersection_index = 0

    @property
    def id(self) -> int:
        return self._id

    @property
    def position(self) -> Vector2D:
        return self._position

    @property
    def direction(self) -> CardinalDirection:
        return self._direction

    def move(self, turn: TurnDirection) -> None:
        self._direction = self._direction.turn(turn)
        self._position = self._position.move(self._direction, y_grows_down=True)

    def pop_next_intersection_turn(self) -> TurnDirection:
        turn = self._intersection_sequence[self._current_intersection_index]
        self._current_intersection_index = (self._current_intersection_index + 1) % len(
            self._intersection_sequence
        )
        return turn

    def __repr__(self) -> str:
        id_as_letter = chr(ord("A") + self._id)
        return f"{id_as_letter}: {self._position.x}"


class MineCarts:
    def __init__(
        self,
        mine_layout: str,
        intersection_sequence: Optional[list[TurnDirection]] = None,
    ) -> None:
        if intersection_sequence is None:
            intersection_sequence = [TurnDirection.NO_TURN]
        self._rows = []
        self._carts = []
        cart_id = 0
        for y, row in enumerate(mine_layout.split("\n")):
            self._rows.append([])
            for x, char in enumerate(row):
                direction = None
                if char == "<":
                    direction = CardinalDirection.WEST
                    self._rows[y].append("-")
                elif char == ">":
                    direction = CardinalDirection.EAST
                    self._rows[y].append("-")
                elif char == "^":
                    direction = CardinalDirection.NORTH
                    self._rows[y].append("|")
                elif char == "v":
                    direction = CardinalDirection.SOUTH
                    self._rows[y].append("|")
                else:
                    self._rows[y].append(char)
                if direction:
                    self._carts.append(
                        _MineCart(
                            cart_id, Vector2D(x, y), direction, intersection_sequence
                        )
                    )
                    cart_id += 1

    @property
    def cart_positions(self) -> Iterator[Vector2D]:
        yield from (cart.position for cart in self._carts)

    def _move_cart(self, cart: _MineCart) -> None:
        track = self._rows[cart.position.y][cart.position.x]
        if track in "|-":
            turn = TurnDirection.NO_TURN
        elif track == "/":
            turn = (
                TurnDirection.RIGHT
                if cart.direction.is_vertical
                else TurnDirection.LEFT
            )
        elif track == "\\":
            turn = (
                TurnDirection.LEFT
                if cart.direction.is_vertical
                else TurnDirection.RIGHT
            )
        elif track == "+":
            turn = cart.pop_next_intersection_turn()
        cart.move(turn)

    def tick(self) -> None:
        for cart in self._carts:
            self._move_cart(cart)

    def _sorted_carts(self) -> Iterator[_MineCart]:
        yield from sorted(
            self._carts, key=lambda cart: (cart.position.y, cart.position.x)
        )

    def collisions(self) -> Iterator[Vector2D]:
        while len(self._carts) > 1:
            carts_to_remove = set()
            occupied_positions = {cart.position: cart.id for cart in self._carts}
            for cart in self._sorted_carts():
                if cart.id in carts_to_remove:
                    continue
                occupied_positions.pop(cart.position, None)
                self._move_cart(cart)
                if cart.position in occupied_positions:
                    yield cart.position
                    carts_to_remove.add(cart.id)
                    carts_to_remove.add(occupied_positions[cart.position])
                    occupied_positions.pop(cart.position, None)
                else:
                    occupied_positions[cart.position] = cart.id
            self._carts = [
                cart for cart in self._carts if cart.id not in carts_to_remove
            ]
