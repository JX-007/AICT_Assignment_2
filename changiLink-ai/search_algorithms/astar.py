import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
	sys.path.append(PROJECT_ROOT)

from Classes.transfer import load_transfer_timings
from mrtNetwork import build_mrt_network
# from  _ import heuristics
import heapq
from heuristics import HEURISTIC_FUNCTIONS

def a_star(mrt_network, start_name, goal_name, heuristic_name="straight_line"):
    import heapq
    from heuristics import HEURISTIC_FUNCTIONS

    start = mrt_network[start_name]
    goal = mrt_network[goal_name]
    heuristic = HEURISTIC_FUNCTIONS[heuristic_name]

    open_set = []
    # (f_score, tie_breaker, station, path, g_score)
    heapq.heappush(
        open_set,
        (heuristic(start, goal), start.name, start, [start_name], 0)
    )

    visited = set()
    nodes_expanded = 0
    max_memory = len(open_set)

    while open_set:
        f, _, current, path, g = heapq.heappop(open_set)

        if current in visited:
            continue

        visited.add(current)
        nodes_expanded += 1
        max_memory = max(max_memory, len(open_set) + len(visited))

        if current == goal:
            return path, nodes_expanded, max_memory

        for neighbor, _lines in current.get_connections():
            if neighbor not in visited:
                g_new = g + 1  # uniform cost per station
                f_new = g_new + heuristic(neighbor, goal)

                heapq.heappush(
                    open_set,
                    (f_new, neighbor.name, neighbor, path + [neighbor.name], g_new)
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

        path, expanded, memory_used = a_star(mrt_network, start, end)

        if path:
            print("Path found:")
            print(" → ".join(path))
        else:
            print("No path found")

        print(f"Nodes expanded: {expanded}")
        print(f"Peak memory usage (nodes): {memory_used}")
