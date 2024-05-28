from typing import Optional
from collections import deque
from models.common.io import ProgressBar


def marble_game_score(
    num_players: int,
    last_marble: int,
    progress_bar: Optional[ProgressBar] = None,
) -> dict[int, int]:
    scores = {i: 0 for i in range(1, num_players + 1)}
    cll = deque([0])
    for marble in range(1, last_marble + 1):
        if progress_bar is not None:
            progress_bar.update(marble, last_marble)
        if marble % 23 == 0:
            cll.rotate(7)
            player_idx = (marble - 1) % num_players + 1
            scores[player_idx] += marble + cll.pop()
            cll.rotate(-1)
        else:
            cll.rotate(-1)
            cll.append(marble)
    return scores
