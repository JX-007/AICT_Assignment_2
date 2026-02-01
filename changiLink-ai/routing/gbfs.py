import os
import sys
import math

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from mrtNetwork import build_mrt_network

def getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates using Haversine formula"""
    R = 6371
    dLat = deg2rad(lat2 - lat1)
    dLon = deg2rad(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d

def deg2rad(deg):
    """Convert degrees to radians"""
    return deg * (math.pi/180)

mrt_speed = 80  # km/h

_missing_coordinate_names = set()

# ============================================================================
# GREEDY BEST-FIRST SEARCH (GBFS) ALGORITHM STEPS
# ============================================================================
# GBFS expands nodes based on heuristic value (h) only, without considering
# accumulated cost (g). It's faster than A* but not guaranteed to find 
# optimal path. Good for quick route suggestions.
# ============================================================================

# STEP 1: Heuristic Function (h-value)
# Estimates distance from current station to goal
def h(station, goal_station):
    """
    STEP 1: Calculate heuristic value
    - Estimates remaining distance to goal using Haversine formula
    - Returns 0 if coordinates missing (admissible heuristic)
    """
    if (
        station is None
        or goal_station is None
        or station.lat is None
        or station.lon is None
        or goal_station.lat is None
        or goal_station.lon is None
    ):
        if station is not None and (station.lat is None or station.lon is None):
            _missing_coordinate_names.add(station.name)
        if goal_station is not None and (goal_station.lat is None or goal_station.lon is None):
            _missing_coordinate_names.add(goal_station.name)
        return 0
    return getDistanceFromLatLonInKm(
        station.lat,
        station.lon,
        goal_station.lat,
        goal_station.lon,
    ) / mrt_speed * 60 * 60  # Convert to seconds


# STEP 2: Priority Queue Implementation
class PriorityQueue:
    """
    STEP 2: Priority Queue for GBFS frontier
    - Stores stations sorted by heuristic value (h)
    - Counter prevents Station object comparison errors
    """
    def __init__(self):
        self.elements = []
        self._counter = 0

    def is_empty(self):
        return not self.elements

    def put(self, item, priority):
        """Add item with priority (lower = better)"""
        self._counter += 1
        self.elements.append((priority, self._counter, item))

    def get(self):
        """Get item with lowest priority"""
        self.elements.sort(key=lambda x: x[0])
        return self.elements.pop(0)[2]


# STEP 3: GBFS Main Algorithm
def gbfs_search(start_station, goal_station):
    """
    STEP 3: Greedy Best-First Search Algorithm
    
    Process:
    a) Initialize frontier with start station
    b) Initialize visited set to track explored stations
    c) Loop while frontier not empty:
       - Get station with lowest h-value from frontier
       - If goal reached, return path
       - Else, expand all neighbors
       - For each neighbor not visited:
         * Add to frontier with h-value as priority
         * Mark parent relationship
    d) Return came_from dict for path reconstruction
    """
    # STEP 3a: Initialize frontier with start station
    frontier = PriorityQueue()
    frontier.put((start_station, None), 0)  # 0 priority for start
    
    # STEP 3b: Track visited stations and parent relationships
    came_from = {}
    visited = set()
    start_key = (start_station, None)
    came_from[start_key] = None

    goal_key = None

    # STEP 3c: Main search loop
    while not frontier.is_empty():
        current_station, current_line = frontier.get()
        current_key = (current_station, current_line)
        
        # Skip if already visited (prevent cycles)
        if current_key in visited:
            continue
        
        visited.add(current_key)

        # Check if goal reached
        if current_station == goal_station:
            goal_key = current_key
            break

        # Expand neighbors
        for next_station, lines in current_station.get_neighbors():
            next_line = current_line if current_line in lines else (lines[0] if lines else current_line)
            next_key = (next_station, next_line)
            
            # Only consider unvisited neighbors
            if next_key not in visited:
                # Priority based on heuristic only (GBFS characteristic)
                priority = h(next_station, goal_station)
                frontier.put((next_station, next_line), priority)
                
                # Record parent if first time seeing this node
                if next_key not in came_from:
                    came_from[next_key] = current_key

    # STEP 3d: Return came_from for path reconstruction
    return came_from, goal_key


# STEP 4: Path Reconstruction with Time Calculation
def reconstruct_path(came_from, end_key):
    """
    STEP 4: Reconstruct path from goal back to start
    - Backtrace through came_from dictionary
    - Reverse to get start → goal order
    - Calculate total travel time along the path
    """
    if end_key is None:
        return [], 0
    
    path = []
    current = end_key
    while current is not None:
        station, line = current
        path.append((station, line))
        current = came_from.get(current)
    path.reverse()
    
    # Calculate total travel time
    total_time = 0
    for i in range(len(path) - 1):
        current_station, current_line = path[i]
        next_station, _ = path[i + 1]
        total_time += current_station.cost_to(next_station, current_line)
    
    station_names = [station.name for station, _ in path]
    return station_names, total_time


# STEP 5: Main Execution
if __name__ == "__main__":
    print("=== GREEDY BEST-FIRST SEARCH (GBFS) ===\n")
    
    # STEP 5a: Build MRT networ
    mrt_network = build_mrt_network()
    
    # STEP 5b: Get user input
    start_station_name = input("Enter start station: ").strip()
    start_station = mrt_network[start_station_name]
    goal_station_name = input("Enter goal station: ").strip()
    goal_station = mrt_network[goal_station_name]
    
    # STEP 5c: Run GBFS
    came_from, goal_key = gbfs_search(start_station, goal_station)
    
    # STEP 5d: Reconstruct and display path
    path, total_time = reconstruct_path(came_from, goal_key)
    if path:
        print("Path found:")
        print(" → ".join(path))
        print(f"Total time: {int(total_time)//3600}:{(int(total_time)%3600)//60:02d}:{int(total_time)%60:02d} (hh:mm:ss)")
    else:
        print("No path found.")

    # STEP 5e: Display missing coordinates (if any)
    if _missing_coordinate_names:
        print("\nMissing coordinates for:")
        for name in sorted(_missing_coordinate_names):
            print(f"- {name}")

# Funnily I started with aStar Search first