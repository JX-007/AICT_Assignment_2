import os
import sys
import math

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from mrtNetwork import build_mrt_network
def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
  R = 6371
  dLat = deg2rad(lat2-lat1)
  dLon = deg2rad(lon2-lon1)
  a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c
  return d


def deg2rad(deg) :
  return deg * (math.pi/180)

mrt_speed = 80 # km/h

_missing_coordinate_names = set()

# Heuristic FUnction
def h(station, goal_station):
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
    ) / mrt_speed * 60 * 60
# Cost function
def g(current_cost, current_station, next_station, current_line=None):
    return current_cost + current_station.cost_to(next_station, current_line)

# Combined cost function
def f(g_cost, station, goal_station):
    return g_cost + h(station, goal_station)
#  Priority Queue Implementation
class PriorityQueue:
    def __init__(self):
        self.elements = []
        self._counter = 0

    def is_empty(self):
        return not self.elements

    def put(self, item, priority):
        self._counter += 1
        self.elements.append((priority, self._counter, item))

    def get(self):
        self.elements.sort(key=lambda x: x[0])
        return self.elements.pop(0)[2]
    
 

# A* Search Algorithm Implementation
def a_star_search(start_station, goal_station):
    frontier = PriorityQueue()
    frontier.put((start_station, None), 0)
    came_from = {}
    cost_so_far = {}
    start_key = (start_station, None)
    came_from[start_key] = None
    cost_so_far[start_key] = 0

    goal_key = None

    while not frontier.is_empty():
        current_station, current_line = frontier.get()
        current_key = (current_station, current_line)

        if current_station == goal_station:
            goal_key = current_key
            break

        for next_station, lines in current_station.get_neighbors():
            next_line = current_line if current_line in lines else (lines[0] if lines else current_line)
            new_cost = g(cost_so_far[current_key], current_station, next_station, current_line)
            next_key = (next_station, next_line)
            if next_key not in cost_so_far or new_cost < cost_so_far[next_key]:
                cost_so_far[next_key] = new_cost
                priority = f(new_cost, next_station, goal_station)
                frontier.put((next_station, next_line), priority)
                came_from[next_key] = current_key

    return came_from, cost_so_far, goal_key


def reconstruct_path(came_from, end_key):
    if end_key is None:
        return []
    path = []
    current = end_key
    while current is not None:
        station, _line = current
        path.append(station.name)
        current = came_from.get(current)
    path.reverse()
    return path

# Main
if __name__ == "__main__":
    mrt_network = build_mrt_network()   
    start_station = input("Enter start station: ")
    start_station = mrt_network[start_station]
    goal_station = input("Enter goal station: ")
    goal_station = mrt_network[goal_station]
    came_from, cost_so_far, goal_key = a_star_search(start_station, goal_station)
    path = reconstruct_path(came_from, goal_key)
    if path:
        print("Path found:")
        print(" → ".join(path))
        print(f"Total time : {cost_so_far[goal_key]//3600}:{(cost_so_far[goal_key]%3600)//60:02d}:{cost_so_far[goal_key]%60:02d} (hh:mm:ss)")
    else:
        print("No path found.")

    if _missing_coordinate_names:
        print("Missing coordinates for:")
        for name in sorted(_missing_coordinate_names):
            print(f"- {name}")