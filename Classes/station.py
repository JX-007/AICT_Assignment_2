
class Station:
	"""
	Represents an MRT station node in the network graph.
	
	Attributes:
		name (str): Station name (e.g., "Jurong East")
		lines (list): MRT lines serving this station (e.g., ["NSL", "EWL"])
		connections (list): List of (Station, travel_time, line_list) tuples
			- Station: Connected station object
			- travel_time (float): Travel time in seconds to connected station
			- line_list (list): Which lines serve this connection
	"""
	
	def __init__(self, name, lines=None):
		"""
		Initialize a Station.
		
		Args:
			name (str): Name of the station
			lines (list, optional): List of lines serving this station
		"""
		self.name = name
		self.lines = lines if lines else []
		self.connections = []  # List of (Station, travel_time, lines) tuples
	
	def add_connection(self, destination_station, travel_time, lines):
		"""
		Add a connection to another station.
		
		Args:
			destination_station (Station): The connected station
			travel_time (float): Travel time to destination in seconds
			lines (list): List of MRT lines used for this connection
		"""
		self.connections.append((destination_station, travel_time, lines))
	
	def get_connections(self):
		"""Returns list of (destination_station, travel_time, lines)."""
		return self.connections
	
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
		for dest_station, weight, lines in station.get_connections():
			# Check if reverse edge exists in destination station
			reverse_edge_found = False
			for reverse_dest, reverse_weight, reverse_lines in dest_station.get_connections():
				if reverse_dest == station and reverse_weight == weight:
					reverse_edge_found = True
					break
			if not reverse_edge_found:
				asymmetric_edges.append(f"{station_name} -> {dest_station.name} (weight: {weight})")
	
	return asymmetric_edges

