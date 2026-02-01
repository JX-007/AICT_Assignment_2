import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
	sys.path.append(PROJECT_ROOT)

from Classes.transfer import load_transfer_timings
from mrtNetwork import build_mrt_network

def breadth_first_search(mrt_network, start_station_name, goal_station_name):
	"""
	Performs breadth-first search to find shortest path by number of stations.
	
	Args:
		mrt_network (dict): Dictionary of Station objects representing the MRT network
		start_station_name (str): Name of the starting station
		goal_station_name (str): Name of the goal station
	
	Returns:
		list: Path from start to goal as list of station names
	"""
	from collections import deque
	
	# Get starting station
	if start_station_name not in mrt_network:
		print(f"Error: Start station '{start_station_name}' not found in network")
		return None, 0, 0
	if goal_station_name not in mrt_network:
		print(f"Error: Goal station '{goal_station_name}' not found in network")
		return None, 0, 0
	
	start_station = mrt_network[start_station_name]
	goal_station = mrt_network[goal_station_name]
	
	if start_station_name == goal_station_name:
		return [start_station_name], 0, 1
	
	visited = set([start_station])
	queue = deque([(start_station, [start_station_name])])
	nodes_expanded = 0
	
	while queue:
		current_station, path = queue.popleft()
		nodes_expanded += 1
		
		# Get all neighboring stations
		for neighbor_station, _lines in current_station.get_neighbors():
			if neighbor_station not in visited:
				if neighbor_station == goal_station:
					final_path = path + [neighbor_station.name]
					total_time = 0
					for i in range(len(final_path) - 1):
						current = mrt_network[final_path[i]]
						next_station = mrt_network[final_path[i + 1]]
						total_time += current.cost_to(next_station, None)
					return final_path, total_time, nodes_expanded
				
				visited.add(neighbor_station)
				queue.append((neighbor_station, path + [neighbor_station.name]))
	
	# No path found
	print(f"No path found from {start_station_name} to {goal_station_name}")
	return None, 0, nodes_expanded



if __name__ == "__main__":
	mode_input = input("(Today or Future)Mode: ").strip().lower()
	mode = "Future" if mode_input == "future" else "Today"

	mrt_network = build_mrt_network(mode=mode)
	transfer_csv = os.path.join(PROJECT_ROOT, "Data", "MRT transfer timing.csv")
	load_transfer_timings(transfer_csv)
	start = "Clementi"
	end = "Changi Airport"

	start_time = time.perf_counter()
	path, total_time, nodes_expanded = breadth_first_search(mrt_network, start, end)
	elapsed = time.perf_counter() - start_time

	if path:
		print(" → ".join(path))
		print(f"Total time: {int(total_time)//3600}:{(int(total_time)%3600)//60:02d}:{int(total_time)%60:02d} (hh:mm:ss)")
		print(f"Path length: {len(path)}")
	else:
		print(f"No path found from {start} to {end}")
	print(f"Nodes expanded: {nodes_expanded}")
	print(f"Runtime: {elapsed:.6f}s")