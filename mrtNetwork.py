import csv
import os
from collections import defaultdict
from Classes.station import Station, checkSymmetry

def load_mrt_connections(csv_path=None):
	"""Load MRT/LRT connections from mrt_connections.csv."""
	if csv_path is None:
		csv_path = os.path.join(os.path.dirname(__file__), "Data", "mrt_connections.csv")

	if not os.path.exists(csv_path):
		raise FileNotFoundError(f"CSV not found: {csv_path}")

	connections_map = defaultdict(lambda: defaultdict(set))

	with open(csv_path, "r", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			station = row.get("Station")
			destination = row.get("Destination")
			line = row.get("Line")
			if not station or not destination or not line:
				continue

			try:
				travel_time = int(row.get("Travel_Time_Seconds", 0))
			except ValueError:
				travel_time = 0

			connections_map[station][(destination, travel_time)].add(line)

	mrt_network_data = {}
	for station, dest_map in connections_map.items():
		connections = []
		for (destination, travel_time), lines in dest_map.items():
			connections.append((destination, travel_time, sorted(lines)))
		mrt_network_data[station] = connections

	return mrt_network_data

CurrentStations = load_mrt_connections()

def build_mrt_network():
	"""
	Builds the MRT network graph with Station objects.
	Returns a dictionary where keys are station names and values are Station objects
	with connections to other stations.
	
	All travel times are in seconds. Baseline station-to-station travel time with penalties as applicable.
	"""
	
	# Consolidated MRT Network Data with stations and their connections
	mrt_network_data = CurrentStations
	
	# Create all Station objects and build connections in a single pass
	mrt_network = {}
	
	# First pass: Create all Station objects with their lines
	for station_name in mrt_network_data.keys():
		# Extract lines from connections by looking at the network
		lines_set = set()
		for dest_name, travel_time, line_list in mrt_network_data[station_name]:
			lines_set.update(line_list)
		
		mrt_network[station_name] = Station(station_name, list(lines_set))
	
	# Second pass: Add connections between Station objects
	for source_name, connections_list in mrt_network_data.items():
		source_station = mrt_network[source_name]
		for dest_name, travel_time, lines in connections_list:
			if dest_name in mrt_network:
				dest_station = mrt_network[dest_name]
				source_station.add_connection(dest_station, travel_time, lines)
	
	return mrt_network
