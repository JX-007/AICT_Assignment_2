import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
	sys.path.append(PROJECT_ROOT)

from Classes.transfer import load_transfer_timings
from mrtNetwork import build_mrt_network

def breadth_first_search(mrt_network, start_station_name, goal_station_name, transfer_timings_dict=None):
	"""
	Performs breadth-first search to find shortest path by travel time (in seconds).
	
	Args:
		mrt_network (dict): Dictionary of Station objects representing the MRT network
		start_station_name (str): Name of the starting station
		goal_station_name (str): Name of the goal station
		transfer_timings_dict (dict): Optional dictionary of transfer timings in seconds for computing penalties
	
	Returns:
		list: Path from start to goal as list of station names
	"""
	from collections import deque
	
	# Get starting station
	if start_station_name not in mrt_network:
		print(f"Error: Start station '{start_station_name}' not found in network")
		return None
	if goal_station_name not in mrt_network:
		print(f"Error: Goal station '{goal_station_name}' not found in network")
		return None
	
	start_station = mrt_network[start_station_name]
	goal_station = mrt_network[goal_station_name]
	
	if start_station_name == goal_station_name:
		return [start_station_name]
	
	visited = set([start_station])
	queue = deque([(start_station, [start_station_name])])
	
	while queue:
		current_station, path = queue.popleft()
		
		# Get all neighboring stations
		for neighbor_station, in current_station.get_connections():
			if neighbor_station not in visited:
				if neighbor_station == goal_station:
					return path + [neighbor_station.name]
				
				visited.add(neighbor_station)
				queue.append((neighbor_station, path + [neighbor_station.name]))
	
	# No path found
	print(f"No path found from {start_station_name} to {goal_station_name}")
	return None



if __name__ == "__main__":
	mrt_network = build_mrt_network()
	transfer_csv = os.path.join(PROJECT_ROOT, "Data", "MRT transfer timing.csv")
	load_transfer_timings(transfer_csv)
	# Example: Find path from Clementi to Changi Airport
	start = "Clementi"
	end = "Changi Airport"
	path = breadth_first_search(mrt_network, start, end)
	
	if path:
		print(f"Path found: {start} → {end}")
		print(" → ".join(path))
	else:
		print(f"No path found from {start} to {end}")