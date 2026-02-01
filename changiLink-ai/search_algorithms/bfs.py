import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
	sys.path.append(PROJECT_ROOT)

import sys
from collections import deque

def breadth_first_search(network, start_name, goal_name, heuristic=None):
    frontier = deque([start_name])
    explored = set()
    parent = {}
    expanded = 0

    while frontier:
        current = frontier.popleft()
        expanded += 1

        if current == goal_name:
            # reconstruct path
            path = [current]
            while current in parent:
                current = parent[current]
                path.append(current)
            return path[::-1], expanded, sys.getsizeof(frontier) + sys.getsizeof(explored)

        explored.add(current)

        for neighbor, _ in network[current].get_connections():
            if neighbor.name not in explored and neighbor.name not in frontier:
                frontier.append(neighbor.name)
                parent[neighbor.name] = current

    return None, expanded, sys.getsizeof(frontier) + sys.getsizeof(explored)
