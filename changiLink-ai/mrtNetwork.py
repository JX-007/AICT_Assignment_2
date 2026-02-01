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

			connections_map[station][destination].add(line)

	mrt_network_data = {}
	for station, dest_map in connections_map.items():
		connections = []
		for destination, lines in dest_map.items():
			connections.append((destination, sorted(lines)))
		mrt_network_data[station] = connections

	return mrt_network_data

def build_mrt_network(mrt_network_data):
    """
    Builds the MRT network graph with Station objects.
    Expects raw network data (station -> [(destination, lines)]).
    """

    mrt_network = {}

    # First pass: create Station objects
    for station_name in mrt_network_data.keys():
        lines_set = set()
        for dest_name, line_list in mrt_network_data[station_name]:
            lines_set.update(line_list)

        mrt_network[station_name] = Station(station_name, list(lines_set))

    # Second pass: add connections
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
