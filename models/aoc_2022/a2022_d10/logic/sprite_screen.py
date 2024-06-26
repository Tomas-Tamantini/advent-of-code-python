class SpriteScreen:
    def __init__(self, width: int, height: int, sprite_length: int) -> None:
        self._width = width
        self._height = height
        self._sprite_half_length = sprite_length // 2

    def draw(self, sprite_center_positions: list[int]) -> str:
        rendered = []
        current_cycle = 0
        for _ in range(self._height):
            current_row = ""
            for col in range(self._width):
                sprite_center_position = (
                    sprite_center_positions[current_cycle]
                    if current_cycle < len(sprite_center_positions)
                    else sprite_center_positions[-1]
                )
                current_row += (
                    "#"
                    if abs(sprite_center_position - col) <= self._sprite_half_length
                    else " "
                )
                current_cycle += 1
            rendered.append(current_row)
        return "\n".join(rendered)
