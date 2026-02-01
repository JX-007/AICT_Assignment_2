import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
	sys.path.append(PROJECT_ROOT)

from Classes.transfer import load_transfer_timings
from mrtNetwork import build_mrt_network

import heapq
from heuristics import HEURISTIC_FUNCTIONS

def gbfs(mrt_network, start_name, goal_name, heuristic_name="straight_line"):
    start = mrt_network[start_name]
    goal = mrt_network[goal_name]
    heuristic = HEURISTIC_FUNCTIONS[heuristic_name]

    open_set = []
    visited = set()
    nodes_expanded = 0

    # (heuristic, tie_breaker, station, path)
    heapq.heappush(
        open_set,
        (heuristic(start, goal), start.name, start, [start_name])
    )

    max_memory = len(open_set)

    while open_set:
        _, _, current, path = heapq.heappop(open_set)

        if current in visited:
            continue

        visited.add(current)
        nodes_expanded += 1
        max_memory = max(max_memory, len(open_set) + len(visited))

        if current == goal:
            return path, nodes_expanded, max_memory

        for neighbor, _lines in current.get_connections():
            if neighbor not in visited:
                heapq.heappush(
                    open_set,
                    (heuristic(neighbor, goal),
                     neighbor.name,
                     neighbor,
                     path + [neighbor.name])
                )

    return None, nodes_expanded, max_memory

if __name__ == "__main__":
    mrt_network = build_mrt_network()
    transfer_csv = os.path.join(PROJECT_ROOT, "Data", "MRT transfer timing.csv")
    load_transfer_timings(transfer_csv)

    start = "Changi Airport"
    destinations = [
        "City Hall",
        "Orchard",
        "Gardens by the Bay",
        "Bugis",
        "HarbourFront"
    ]

    for end in destinations:
        print("\n" + "=" * 50)
        print(f"Testing route: {start} → {end}")

        path, expanded, memory_used = gbfs(mrt_network, start, end)

        if path:
            print("Path found:")
            print(" → ".join(path))
        else:
            print("No path found")

        print(f"Nodes expanded: {expanded}")
        print(f"Peak memory usage (nodes): {memory_used}")
