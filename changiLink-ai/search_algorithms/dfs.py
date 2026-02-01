import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
	sys.path.append(PROJECT_ROOT)

from Classes.transfer import load_transfer_timings
from mrtNetwork import build_mrt_network

def depth_first_search(mrt_network, start_station_name, goal_station_name):
    """
    Iterative DFS: returns path, nodes expanded, peak memory (stack + visited)
    """
    if start_station_name not in mrt_network or goal_station_name not in mrt_network:
        return None, 0, 0

    start_station = mrt_network[start_station_name]
    goal_station = mrt_network[goal_station_name]

    visited = set()
    stack = [(start_station, [start_station_name])]

    nodes_expanded = 0
    max_memory = len(stack) + len(visited)

    while stack:
        current_station, path = stack.pop()
        nodes_expanded += 1
        visited.add(current_station)

        # update peak memory usage
        current_memory = len(stack) + len(visited)
        max_memory = max(max_memory, current_memory)

        if current_station == mrt_network[goal_station_name]:
            return path, nodes_expanded, max_memory

        # push neighbors (can sort if you want deterministic order)
        for neighbor_station, _lines in reversed(current_station.get_connections()):
            if neighbor_station not in visited:
                stack.append((neighbor_station, path + [neighbor_station.name]))

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
        print("\n" + "="*50)
        print(f"Testing DFS route: {start} → {end}")

        path, expanded, memory_used = depth_first_search(mrt_network, start, end)

        if path:
            print("Path found:")
            print(" → ".join(path))
        else:
            print("No path found")

        print(f"Nodes expanded: {expanded}")
        print(f"Peak memory usage (nodes): {memory_used}")

