from typing import Iterator, Optional
from models.vectors import Vector2D, CardinalDirection, TurnDirection


class _MineCart:
    def __init__(
        self,
        position: Vector2D,
        direction: CardinalDirection,
        intersection_sequence: list[TurnDirection],
    ) -> None:
        self._position = position
        self._direction = direction
        self._intersection_sequence = intersection_sequence
        self._current_intersection_index = 0

    @property
    def position(self) -> Vector2D:
        return self._position

    @property
    def direction(self) -> CardinalDirection:
        return self._direction

    def move(self, turn: TurnDirection) -> None:
        self._direction = self._direction.turn(turn)
        mirrored_direction = (
            self._direction
            if self._direction.is_horizontal
            else self._direction.reverse()
        )
        self._position = self._position.move(mirrored_direction)

    def pop_next_intersection_turn(self) -> TurnDirection:
        turn = self._intersection_sequence[self._current_intersection_index]
        self._current_intersection_index = (self._current_intersection_index + 1) % len(
            self._intersection_sequence
        )
        return turn


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
                        _MineCart(Vector2D(x, y), direction, intersection_sequence)
                    )

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
        while True:
            occupied_positions = set(self.cart_positions)
            for cart in self._sorted_carts():
                occupied_positions.remove(cart.position)
                self._move_cart(cart)
                if cart.position in occupied_positions:
                    yield cart.position
                occupied_positions.add(cart.position)
