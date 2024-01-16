from math import sqrt, floor


class SquareSpiral:
    @staticmethod
    def _layer_start(layer_idx: int) -> int:
        return (2 * layer_idx - 1) ** 2 + 1

    @staticmethod
    def _arm_length(layer_idx: int) -> int:
        return 2 * layer_idx

    @staticmethod
    def coordinates(index: int) -> tuple[int, int]:
        if index == 1:
            return (0, 0)
        layer_idx = floor((sqrt(index - 1) + 1) / 2)
        arm_length = SquareSpiral._arm_length(layer_idx)
        offset = index - SquareSpiral._layer_start(layer_idx)
        if offset < arm_length:
            return (layer_idx, offset - layer_idx + 1)
        elif offset < 2 * arm_length:
            return (layer_idx - (offset - arm_length + 1), layer_idx)
        elif offset < 3 * arm_length:
            return (-layer_idx, layer_idx - (offset - 2 * arm_length + 1))
        else:
            return (
                -layer_idx + (offset - 3 * arm_length + 1),
                -layer_idx,
            )

    @staticmethod
    def spiral_index(x: int, y: int) -> int:
        layer_idx = max(abs(x), abs(y))
        if layer_idx == 0:
            return 1
        layer_start = SquareSpiral._layer_start(layer_idx)
        arm_length = SquareSpiral._arm_length(layer_idx)
        offset = layer_start + layer_idx - 1
        if x == layer_idx and y > -layer_idx:
            return offset + y
        elif y == layer_idx and x < layer_idx:
            return offset + arm_length - x
        elif x == -layer_idx and y < layer_idx:
            return offset + 2 * arm_length - y
        else:
            return offset + 3 * arm_length + x
