from typing import Protocol, Iterator


class _Node(Protocol):
    def neighboring_valid_states(self) -> Iterator["_Node"]:
        ...

    def is_final_state(self) -> bool:
        ...


def min_path_length_with_bfs(initial_node: _Node) -> int:
    if initial_node.is_final_state():
        return 0
    queue = [(initial_node, 0)]
    visited = {initial_node}
    while queue:
        node, distance = queue.pop(0)
        for neighbor in node.neighboring_valid_states():
            if neighbor.is_final_state():
                return distance + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    raise ValueError("No path to final state found")
