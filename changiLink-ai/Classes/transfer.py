import csv

class Transfer:
	"""
	Represents transfer timing data between two MRT stations.
	
	Attributes:
		station_from (str): Starting station name
		station_to (str): Destination station name
		line_from (str): Starting line code (e.g., "NSL")
		line_to (str): Destination line code (e.g., "EWL")
		code_from (str): Station code on starting line (e.g., "NS1")
		code_to (str): Station code on destination line (e.g., "EW24")
		transfer_time (int): Transfer time in seconds
	
	Suggested Additional Fields:
		- station_pair_id: Tuple (from, to) for quick lookup
	"""
	
	def __init__(self, station_from, line_from, code_from, 
	             station_to, line_to, code_to, transfer_time_seconds):
		"""
		Initialize a Transfer.
		
		Args:
			station_from (str): Starting station name
			line_from (str): Starting MRT line (e.g., "NSL")
			code_from (str): Starting station code (e.g., "NS1")
			station_to (str): Destination station name
			line_to (str): Destination MRT line (e.g., "EWL")
			code_to (str): Destination station code (e.g., "EW24")
			transfer_time_seconds (int): Transfer time in seconds
		"""
		self.station_from = station_from
		self.line_from = line_from
		self.code_from = code_from
		self.station_to = station_to
		self.line_to = line_to
		self.code_to = code_to
		self.transfer_time_seconds = transfer_time_seconds
		self.transfer_time_minutes = transfer_time_seconds / 60.0
		
		# Additional suggested fields for future enhancements
		self.station_pair_id = (station_from, station_to, line_from, line_to)
	
	def __repr__(self):
		"""String representation of the Transfer."""
		return (f"Transfer({self.station_from} {self.line_from}->{self.station_to} "
		        f"{self.line_to}: {self.transfer_time_seconds}sec)")
	
	def __str__(self):
		"""String representation."""
		return (f"{self.station_from} ({self.line_from}{self.code_from}) → "
		        f"{self.station_to} ({self.line_to}{self.code_to}): ")
	
	def __lt__(self, other):
		"""Allow sorting transfers by transfer time."""
		return self.transfer_time_seconds < other.transfer_time_seconds

def load_transfer_timings(csv_file_path):
	"""
	Load MRT transfer timing data from CSV file and create Transfer objects.
	"""
	transfers_dict = {}
	transfers_list = []
	
	try:
		with open(csv_file_path, 'r', encoding='utf-8-sig') as file:  # utf-8-sig removes BOM
			reader = csv.DictReader(file)
			row_count = 0
			skipped_count = 0
			
			for row in reader:
				row_count += 1
				try:
					# Extract station name with robust fallback logic
					station_name = row.get('Station Name', '').strip()
					if not station_name:
						# Fallback: Search through all columns for valid station name
						for column_header, cell_value in row.items():
							candidate = (cell_value or '').strip()
							# Filter out line codes, station codes, and empty values
							if (candidate and 
								candidate not in ["NSL", "EWL", "NEL", "CCL", "DTL", "TEL", "BPLRT", "SKLRT", "PGLRT"] and
								not candidate[0].isdigit() and 
								len(candidate) > 2):
								station_name = candidate
								break
					
					# Extract line and station code information
					line_from = row.get('Start Line', '').strip()
					code_from = row.get('Start Code', '').strip()
					line_to = row.get('End Line', '').strip()
					code_to = row.get('End Code', '').strip()
					transfer_time_str = row.get('Transfer time in seconds', '').strip()
					
					# Validate all required fields are present
					if not all([station_name, line_from, code_from, line_to, code_to, transfer_time_str]):
						skipped_count += 1
						continue
					
					# Convert transfer time to integer (seconds)
					transfer_time = int(transfer_time_str)
					
					# Both directions use same station (transfer between lines at same station)
					station_from = station_name
					station_to = station_name
					
					# Create Transfer object with calculated difficulty rating
					transfer = Transfer(
						station_from=station_from,
						line_from=line_from,
						code_from=code_from,
						station_to=station_to,
						line_to=line_to,
						code_to=code_to,
						transfer_time_seconds=transfer_time
					)
					
					# Store in dictionary for O(1) lookup
					# Key: (station_from, station_to, line_from, line_to)
					key = (station_from, station_to, line_from, line_to)
					transfers_dict[key] = transfer
					transfers_list.append(transfer)
				
				except (ValueError, KeyError, TypeError) as e:
					skipped_count += 1
					continue
		
		# Summary statistics
		print(f"✓ Transfer Timing Loader - Summary:")
		print(f"  • Loaded {len(transfers_list)} transfer records")
		print(f"  • Processed {row_count} rows (skipped {skipped_count})")
		if transfers_list:
			times = sorted([t.transfer_time_seconds for t in transfers_list])
			print(f"  • Time range: {times[0]}s to {times[-1]}s (avg: {sum(times)//len(times)}s)")
		
		return transfers_dict, transfers_list
	
	except FileNotFoundError:
		print(f"✗ Transfer timing CSV file not found: {csv_file_path}")
		print(f"  Expected file at: {csv_file_path}")
		print(f"  Please ensure 'MRT transfer timing.csv' exists in the working directory")
		return {}, []
	
	except Exception as e:
		print(f"✗ Error loading transfer timings: {e}")
		print(f"  File: {csv_file_path}")
		print(f"  Error type: {type(e).__name__}")
		import traceback
		traceback.print_exc()
		return {}, []

