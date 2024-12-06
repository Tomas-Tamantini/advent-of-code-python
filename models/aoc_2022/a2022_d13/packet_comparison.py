from typing import Union


def left_packet_leq_right(
    left_packet: Union[list, int], right_packet: Union[list, int]
) -> bool:
    if isinstance(left_packet, int):
        if isinstance(right_packet, int):
            return left_packet <= right_packet
        else:
            return left_packet_leq_right([left_packet], right_packet)
    elif isinstance(right_packet, int):
        return left_packet_leq_right(left_packet, [right_packet])
    else:
        for left, right in zip(left_packet, right_packet):
            left_lt = left_packet_leq_right(left, right)
            right_lt = left_packet_leq_right(right, left)
            if left_lt and not right_lt:
                return True
            elif right_lt and not left_lt:
                return False
        return len(left_packet) <= len(right_packet)
