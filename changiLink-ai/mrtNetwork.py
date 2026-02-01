import csv
import os
from collections import defaultdict
from Classes.station import Station, checkSymmetry


def load_station_coordinates(csv_path=None):
	"""Load station coordinates from mrt_lrt_data.csv.

	Supports both schemas:
	- station_name,type,lat,lng
	- station_name,lat,lng

	Returns a dict: {station_name: (longitude, latitude)}
	"""
	if csv_path is None:
		csv_path = os.path.join(os.path.dirname(__file__), "Data", "mrt_lrt_data.csv")

	if not os.path.exists(csv_path):
		raise FileNotFoundError(f"CSV not found: {csv_path}")

	coordinates = {}
	with open(csv_path, "r", encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			name = (row.get("station_name") or "").strip()
			lat = (row.get("lat") or "").strip()
			lng = (row.get("lng") or "").strip()
			if not name:
				continue
			try:
				latitude = float(lat) if lat else None
				longitude = float(lng) if lng else None
			except ValueError:
				latitude = None
				longitude = None
			coordinates[name] = (longitude, latitude)

	return coordinates

def load_mrt_connections(csv_path=None, mode="Today"):
	"""Load MRT/LRT connections from mrt_connections.csv or future_mrt_connections.csv.
	
	Args:
		csv_path: Optional path to CSV file. If None, uses default based on mode.
		mode: String, either "Today" or "Future". Determines which network to load.
			   "Future" mode loads both current and future connections combined.
	"""
	connections_map = defaultdict(lambda: defaultdict(set))
	
	if csv_path is None:
		if mode.lower() == "future":
			# Load both current and future connections for Future mode
			csv_paths = [
				os.path.join(os.path.dirname(__file__), "Data", "mrt_connections.csv"),
				os.path.join(os.path.dirname(__file__), "Data", "future_mrt_connections.csv")
			]
		else:
			# Load only current connections for Today mode
			csv_paths = [os.path.join(os.path.dirname(__file__), "Data", "mrt_connections.csv")]
	else:
		csv_paths = [csv_path]

	# Load connections from all specified CSV files
	for csv_file in csv_paths:
		if not os.path.exists(csv_file):
			raise FileNotFoundError(f"CSV not found: {csv_file}")

		with open(csv_file, "r", encoding="utf-8") as f:
			reader = csv.DictReader(f)
			for row in reader:
				station = row.get("Station")
				destination = row.get("Destination")
				line = row.get("Line")
				if not station or not destination or not line:
					continue

				connections_map[station][destination].add(line)

	mrt_network_data = {}
	for station, dest_map in connections_map.items():
		connections = []
		for destination, lines in dest_map.items():
			connections.append((destination, sorted(lines)))
		mrt_network_data[station] = connections

	return mrt_network_data

CurrentStations = load_mrt_connections()

def build_mrt_network(mode="Today"):
	"""
	Builds the MRT network graph with Station objects.
	Returns a dictionary where keys are station names and values are Station objects
	with connections to other stations.
	
	Args:
		mode: String, either "Today" or "Future". Determines which network to load.
	
	All travel times are in seconds. Baseline station-to-station travel time with penalties as applicable.
	"""
	
	# Consolidated MRT Network Data with stations and their connections
	mrt_network_data = load_mrt_connections(mode=mode)
	
	# Create all Station objects and build connections in a single pass
	mrt_network = {}
	
	# First pass: Create all Station objects with their lines
	for station_name in mrt_network_data.keys():
		# Extract lines from connections by looking at the network
		lines_set = set()
		for dest_name, line_list in mrt_network_data[station_name]:
			lines_set.update(line_list)
		
		mrt_network[station_name] = Station(station_name, list(lines_set))
	
	# Second pass: Add connections between Station objects
	for source_name, connections_list in mrt_network_data.items():
		source_station = mrt_network[source_name]
		for dest_name, lines in connections_list:
			if dest_name in mrt_network:
				dest_station = mrt_network[dest_name]
				source_station.add_connection(dest_station, lines)
	
	return mrt_network

def load_future_mrt_connections(future_csv, base_network_data):
    """
    Merge future MRT stations into existing MRT network data.
    """
    future_data = load_mrt_connections(future_csv)

    for station, connections in future_data.items():
        if station not in base_network_data:
            base_network_data[station] = connections
        else:
            base_network_data[station].extend(connections)

    return base_network_data
