
import time
import tracemalloc

from mrtNetwork import build_mrt_network
from routing.dfs import dfs_search, reconstruct_path as dfs_reconstruct
from routing.gbfs import gbfs_search, reconstruct_path as gbfs_reconstruct
from routing.astar import a_star_search, reconstruct_path as astar_reconstruct
from routing.bfs import breadth_first_search


def format_time(seconds):
	seconds = int(seconds)
	hours = seconds // 3600
	minutes = (seconds % 3600) // 60
	secs = seconds % 60
	return f"{hours}:{minutes:02d}:{secs:02d}"


def run_all_routes(mrt_network, start_station_name, goal_station_name):
	if start_station_name not in mrt_network:
		print(f"Error: Start station '{start_station_name}' not found in network")
		return
	if goal_station_name not in mrt_network:
		print(f"Error: Goal station '{goal_station_name}' not found in network")
		return

	start_station = mrt_network[start_station_name]
	goal_station = mrt_network[goal_station_name]

	results = []

	print("\n=== BREADTH-FIRST SEARCH (BFS) ===")
	tracemalloc.start()
	start_time = time.perf_counter()
	bfs_path, bfs_total_time, bfs_nodes = breadth_first_search(mrt_network, start_station_name, goal_station_name)
	bfs_elapsed = time.perf_counter() - start_time
	_, bfs_peak = tracemalloc.get_traced_memory()
	tracemalloc.stop()
	if bfs_path:
		print("Path found:")
		print(" → ".join(bfs_path))
		print(f"Total time: {format_time(bfs_total_time)} (hh:mm:ss)")
		print(f"Path length: {len(bfs_path)}")
	else:
		print("No path found.")
	print(f"Runtime: {bfs_elapsed:.6f}s")
	print(f"Memory (peak): {bfs_peak / (1024 * 1024):.2f} MB")
	print(f"Nodes expanded: {bfs_nodes}")
	results.append(("BFS", bfs_elapsed, bfs_peak, len(bfs_path) if bfs_path else 0, bfs_nodes))

	print("\n=== DEPTH-FIRST SEARCH (DFS) ===")
	tracemalloc.start()
	start_time = time.perf_counter()
	dfs_came_from, dfs_goal_key, dfs_nodes = dfs_search(start_station, goal_station)
	dfs_elapsed = time.perf_counter() - start_time
	_, dfs_peak = tracemalloc.get_traced_memory()
	tracemalloc.stop()
	dfs_path, dfs_time = dfs_reconstruct(dfs_came_from, dfs_goal_key)
	if dfs_path:
		print("Path found:")
		print(" → ".join(dfs_path))
		print(f"Total time: {format_time(dfs_time)} (hh:mm:ss)")
		print(f"Path length: {len(dfs_path)}")
	else:
		print("No path found.")
	print(f"Runtime: {dfs_elapsed:.6f}s")
	print(f"Memory (peak): {dfs_peak / (1024 * 1024):.2f} MB")
	print(f"Nodes expanded: {dfs_nodes}")
	results.append(("DFS", dfs_elapsed, dfs_peak, len(dfs_path) if dfs_path else 0, dfs_nodes))

	print("\n=== GREEDY BEST-FIRST SEARCH (GBFS) ===")
	tracemalloc.start()
	start_time = time.perf_counter()
	gbfs_came_from, gbfs_goal_key, gbfs_nodes = gbfs_search(start_station, goal_station)
	gbfs_elapsed = time.perf_counter() - start_time
	_, gbfs_peak = tracemalloc.get_traced_memory()
	tracemalloc.stop()
	gbfs_path, gbfs_time = gbfs_reconstruct(gbfs_came_from, gbfs_goal_key)
	if gbfs_path:
		print("Path found:")
		print(" → ".join(gbfs_path))
		print(f"Total time: {format_time(gbfs_time)} (hh:mm:ss)")
		print(f"Path length: {len(gbfs_path)}")
	else:
		print("No path found.")
	print(f"Runtime: {gbfs_elapsed:.6f}s")
	print(f"Memory (peak): {gbfs_peak / (1024 * 1024):.2f} MB")
	print(f"Nodes expanded: {gbfs_nodes}")
	results.append(("GBFS", gbfs_elapsed, gbfs_peak, len(gbfs_path) if gbfs_path else 0, gbfs_nodes))

	print("\n=== A* SEARCH (A*) ===")
	tracemalloc.start()
	start_time = time.perf_counter()
	astar_came_from, astar_costs, astar_goal_key, astar_nodes = a_star_search(start_station, goal_station)
	astar_elapsed = time.perf_counter() - start_time
	_, astar_peak = tracemalloc.get_traced_memory()
	tracemalloc.stop()
	astar_path = astar_reconstruct(astar_came_from, astar_goal_key)
	if astar_path:
		print("Path found:")
		print(" → ".join(astar_path))
		print(f"Total time: {format_time(astar_costs[astar_goal_key])} (hh:mm:ss)")
		print(f"Path length: {len(astar_path)}")
	else:
		print("No path found.")
	print(f"Runtime: {astar_elapsed:.6f}s")
	print(f"Memory (peak): {astar_peak / (1024 * 1024):.2f} MB")
	print(f"Nodes expanded: {astar_nodes}")
	results.append(("A*", astar_elapsed, astar_peak, len(astar_path) if astar_path else 0, astar_nodes))

	print("\n=== SUMMARY ===")
	print(f"{'Algorithm':<10} {'Runtime (s)':>12} {'Memory (MB)':>14} {'Path Len':>10} {'Nodes':>10}")
	for name, elapsed, peak, path_len, nodes in results:
		print(f"{name:<10} {elapsed:>12.6f} {peak / (1024 * 1024):>14.2f} {path_len:>10} {nodes:>10}")


if __name__ == "__main__":
	mode_input = input("(Today or Future)Mode: ").strip().lower()
	mode = "Future" if mode_input == "future" else "Today"
	mrt_network = build_mrt_network(mode=mode)

	start_station_name = input("Enter start station: ").strip()
	goal_station_name = input("Enter goal station: ").strip()

	run_all_routes(mrt_network, start_station_name, goal_station_name)
