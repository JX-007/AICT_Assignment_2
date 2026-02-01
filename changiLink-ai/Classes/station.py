
import os

from Classes.transfer import load_transfer_timings

TRANSFER_AVG_SECONDS = 200
TRANSFER_LINE_CHANGE_PENALTY = 100
BASE_TRAVEL_TIME_SECONDS = 180

_TRANSFER_TIMINGS_CACHE = None


def _get_transfer_timings():
	global _TRANSFER_TIMINGS_CACHE
	if _TRANSFER_TIMINGS_CACHE is None:
		csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "MRT transfer timing.csv")
		transfers_dict, _ = load_transfer_timings(csv_path)
		_TRANSFER_TIMINGS_CACHE = transfers_dict
	return _TRANSFER_TIMINGS_CACHE


def _get_transfer_time_seconds(station_name, line_from, line_to):
	transfers_dict = _get_transfer_timings()
	key = (station_name, station_name, line_from, line_to)
	transfer = transfers_dict.get(key)
	if transfer:
		return transfer.transfer_time_seconds
	return TRANSFER_AVG_SECONDS


class Station:
	"""
	Represents an MRT station node in the network graph.
	
	Attributes:
		name (str): Station name (e.g., "Jurong East")
		lines (list): MRT lines serving this station (e.g., ["NSL", "EWL"])
		connections (list): List of (Station, travel_time, line_list) tuples
				- Station: Connected station object
				- line_list (list): Which lines serve this connection
	"""
	
	def __init__(self, name, lines=None, longitude=None, latitude=None):
		"""
		Initialize a Station.
		
		Args:
			name (str): Name of the station
			lines (list, optional): List of lines serving this station
			longitude (float, optional): Longitude coordinate
			latitude (float, optional): Latitude coordinate
		"""
		self.name = name
		self.lines = lines if lines else []
		self.connections = []  # List of (Station, lines) tuples
		self.longitude = longitude
		self.latitude = latitude
		self.lon = longitude
		self.lat = latitude
	
	def add_connection(self, destination_station, lines):
		"""
		Add a connection to another station.
		
		Args:
			destination_station (Station): The connected station
			lines (list): List of MRT lines used for this connection
		"""
		self.connections.append((destination_station, lines))
	
	def get_neighbors(self):
		"""Returns list of (destination_station, lines)."""
		return self.connections
	
	def cost_to(self, destination_station, current_line=None):
		"""
		Calculate travel time to a destination station.

		Base travel time is 180s. If a line change is required, add transfer time
		(from transfer timing data or default 200s) plus a 100s station change penalty.
		"""
		if destination_station is None:
			return BASE_TRAVEL_TIME_SECONDS

		connection_lines = None
		for neighbor_station, lines in self.connections:
			if neighbor_station == destination_station:
				connection_lines = lines
				break

		if not connection_lines:
			return BASE_TRAVEL_TIME_SECONDS

		if current_line is None or current_line in connection_lines:
			return BASE_TRAVEL_TIME_SECONDS

		transfer_time = min(
			_get_transfer_time_seconds(self.name, current_line, new_line)
			for new_line in connection_lines
		)
		return BASE_TRAVEL_TIME_SECONDS + transfer_time + TRANSFER_LINE_CHANGE_PENALTY
	
	def __repr__(self):
		"""String representation of the Station."""
		lines_str = ",".join(self.lines) if self.lines else "None"
		return f"Station('{self.name}', lines=[{lines_str}], connections={len(self.connections)})"
	
	def __str__(self):
		"""Human-readable string representation."""
		lines_str = " / ".join(self.lines) if self.lines else "No lines"
		return f"{self.name} ({lines_str})"


# Check that all connections are bidirectional: if A->B exists, B->A should also exist
def checkSymmetry(mrt_stations):
	"""Validates that all edges in the graph are bidirectional.
	mrt_stations: dictionary of Station objects
	Returns a list of all asymmetric edges found.
	"""
	asymmetric_edges = []
	for station_name, station in mrt_stations.items():
		for dest_station, lines in station.get_connections():
			# Check if reverse edge exists in destination station
			reverse_edge_found = False
			for reverse_dest, reverse_lines in dest_station.get_connections():
				if reverse_dest == station:
					reverse_edge_found = True
					break
			if not reverse_edge_found:
				asymmetric_edges.append(f"{station_name} -> {dest_station.name}")
	
	return asymmetric_edges

def get_lines_to(self, other_station):
    for dest, lines in self.connections:
        if dest == other_station:
            return lines
    return []

Station.get_lines_to = get_lines_to
