"""
Heuristic functions for informed search algorithms (GBFS and A*).

This module provides:
- Station coordinates (latitude, longitude) for Singapore MRT stations
- Straight-line distance heuristic using Haversine formula
- Heuristic justification and validation
"""

import math

# Singapore MRT Station Coordinates (approximate lat/lon)
# Source: Based on actual station locations, used for heuristic estimation
STATION_COORDINATES = {
    # North-South Line (NSL)
    "Jurong East": (1.3332, 103.7428),
    "Bukit Batok": (1.3490, 103.7497),
    "Bukit Gombak": (1.3588, 103.7517),
    "Choa Chu Kang": (1.3854, 103.7444),
    "Yew Tee": (1.3970, 103.7472),
    "Kranji": (1.4251, 103.7619),
    "Marsiling": (1.4326, 103.7738),
    "Woodlands": (1.4370, 103.7865),
    "Admiralty": (1.4406, 103.8009),
    "Sembawang": (1.4491, 103.8202),
    "Canberra": (1.4430, 103.8296),
    "Yishun": (1.4296, 103.8350),
    "Khatib": (1.4172, 103.8329),
    "Yio Chu Kang": (1.3817, 103.8450),
    "Ang Mo Kio": (1.3700, 103.8495),
    "Bishan": (1.3508, 103.8484),
    "Braddell": (1.3404, 103.8468),
    "Toa Payoh": (1.3327, 103.8476),
    "Novena": (1.3203, 103.8438),
    "Newton": (1.3127, 103.8382),
    "Orchard": (1.3044, 103.8318),
    "Somerset": (1.3002, 103.8389),
    "Dhoby Ghaut": (1.2989, 103.8456),
    "City Hall": (1.2930, 103.8520),
    "Raffles Place": (1.2838, 103.8512),
    "Marina Bay": (1.2761, 103.8542),
    "Marina South Pier": (1.2710, 103.8631),
    
    # East-West Line (EWL)
    "Pasir Ris": (1.3730, 103.9493),
    "Tampines": (1.3537, 103.9452),
    "Simei": (1.3434, 103.9533),
    "Tanah Merah": (1.3276, 103.9464),
    "Bedok": (1.3240, 103.9300),
    "Kembangan": (1.3211, 103.9132),
    "Eunos": (1.3198, 103.9034),
    "Paya Lebar": (1.3177, 103.8926),
    "Aljunied": (1.3164, 103.8826),
    "Kallang": (1.3114, 103.8714),
    "Lavender": (1.3073, 103.8631),
    "Bugis": (1.3006, 103.8556),
    "Tanjong Pagar": (1.2765, 103.8458),
    "Outram Park": (1.2802, 103.8397),
    "Tiong Bahru": (1.2862, 103.8270),
    "Redhill": (1.2895, 103.8172),
    "Queenstown": (1.2942, 103.8059),
    "Commonwealth": (1.3025, 103.7983),
    "Buona Vista": (1.3071, 103.7906),
    "Dover": (1.3114, 103.7785),
    "Clementi": (1.3150, 103.7652),
    "Chinese Garden": (1.3425, 103.7325),
    "Lakeside": (1.3444, 103.7208),
    "Boon Lay": (1.3388, 103.7058),
    "Pioneer": (1.3376, 103.6974),
    "Joo Koon": (1.3277, 103.6782),
    "Gul Circle": (1.3195, 103.6605),
    "Tuas Crescent": (1.3208, 103.6490),
    "Tuas West Road": (1.3300, 103.6395),
    "Tuas Link": (1.3404, 103.6368),
    "Expo": (1.3346, 103.9614),
    "Changi Airport": (1.3573, 103.9886),
    
    # North-East Line (NEL)
    "HarbourFront": (1.2653, 103.8219),
    "Outram Park": (1.2802, 103.8397),
    "Chinatown": (1.2844, 103.8438),
    "Clarke Quay": (1.2886, 103.8466),
    "Little India": (1.3068, 103.8517),
    "Farrer Park": (1.3121, 103.8535),
    "Boon Keng": (1.3194, 103.8616),
    "Potong Pasir": (1.3311, 103.8687),
    "Woodleigh": (1.3393, 103.8708),
    "Serangoon": (1.3496, 103.8734),
    "Kovan": (1.3604, 103.8849),
    "Hougang": (1.3712, 103.8926),
    "Buangkok": (1.3828, 103.8928),
    "Sengkang": (1.3916, 103.8954),
    "Punggol": (1.4051, 103.9022),
    
    # Circle Line (CCL)
    "Promenade": (1.2932, 103.8611),
    "Nicoll Highway": (1.2998, 103.8634),
    "Stadium": (1.3031, 103.8752),
    "Mountbatten": (1.3065, 103.8823),
    "Dakota": (1.3081, 103.8878),
    "MacPherson": (1.3267, 103.8902),
    "Tai Seng": (1.3358, 103.8881),
    "Bartley": (1.3426, 103.8797),
    "Lorong Chuan": (1.3514, 103.8637),
    "Marymount": (1.3485, 103.8394),
    "Caldecott": (1.3376, 103.8395),
    "Botanic Gardens": (1.3225, 103.8155),
    "Farrer Road": (1.3172, 103.8075),
    "Holland Village": (1.3122, 103.7963),
    "one-north": (1.2996, 103.7874),
    "Kent Ridge": (1.2935, 103.7845),
    "Haw Par Villa": (1.2825, 103.7818),
    "Pasir Panjang": (1.2764, 103.7912),
    "Labrador Park": (1.2721, 103.8023),
    "Telok Blangah": (1.2708, 103.8097),
    "Bayfront": (1.2820, 103.8590),
    "Marina Bay": (1.2761, 103.8542),
    "Keppel": (1.2701, 103.831),
    "Cantonment": (1.272814, 103.836659),
    "Prince Edward Road": (1.273254, 103.847298),
    
    # Downtown Line (DTL)
    "Bukit Panjang": (1.3793, 103.7619),
    "Cashew": (1.3693, 103.7642),
    "Hillview": (1.3628, 103.7676),
    "Beauty World": (1.3413, 103.7757),
    "King Albert Park": (1.3352, 103.7831),
    "Sixth Avenue": (1.3306, 103.7976),
    "Tan Kah Kee": (1.3259, 103.8073),
    "Stevens": (1.3199, 103.8255),
    "Rochor": (1.3039, 103.8525),
    "Little India": (1.3068, 103.8517),
    "Bendemeer": (1.3139, 103.8625),
    "Geylang Bahru": (1.3211, 103.8713),
    "Mattar": (1.3266, 103.8829),
    "Ubi": (1.3300, 103.8964),
    "Kaki Bukit": (1.3348, 103.9089),
    "Bedok North": (1.3347, 103.9185),
    "Bedok Reservoir": (1.3364, 103.9322),
    "Tampines West": (1.3455, 103.9382),
    "Tampines": (1.3537, 103.9452),
    "Tampines East": (1.3563, 103.9545),
    "Upper Changi": (1.3416, 103.9614),
    "Expo": (1.3346, 103.9614),
    
    # Thomson-East Coast Line (TEL)
    "Woodlands North": (1.4482, 103.7859),
    "Woodlands": (1.4370, 103.7865),
    "Woodlands South": (1.4279, 103.7944),
    "Springleaf": (1.4167, 103.8172),
    "Lentor": (1.3847, 103.8362),
    "Mayflower": (1.3657, 103.8380),
    "Bright Hill": (1.3629, 103.8329),
    "Upper Thomson": (1.3548, 103.8303),
    "Caldecott": (1.3376, 103.8395),
    "Mount Pleasant": (1.3263, 103.8350),
    "Stevens": (1.3199, 103.8255),
    "Napier": (1.3113, 103.8159),
    "Orchard Boulevard": (1.3019, 103.8250),
    "Orchard": (1.3044, 103.8318),
    "Great World": (1.2936, 103.8321),
    "Havelock": (1.2887, 103.8352),
    "Outram Park": (1.2802, 103.8397),
    "Maxwell": (1.2801, 103.8445),
    "Shenton Way": (1.2789, 103.8497),
    "Marina Bay": (1.2761, 103.8542),
    "Gardens by the Bay": (1.2812, 103.8636),
    "Tanjong Rhu": (1.2934, 103.8748),
    "Katong Park": (1.3012, 103.8900),
    "Tanjong Katong": (1.3058, 103.8955),
    "Marine Parade": (1.3025, 103.9050),
    "Marine Terrace": (1.3056, 103.9143),
    "Siglap": (1.3138, 103.9267),
    "Bayshore": (1.3208, 103.9391),

    # Future TELe stations
    "T5 Interchange": (1.3650, 104.0150),  # Estimated location
    "Aviation Park": (1.36989, 104.00314),

    # Light Rail Lines
    "Punggol": (1.4051, 103.9022),
    "Sengkang": (1.3916, 103.8954),
    "Choa Chu Kang": (1.3854, 103.7444),
}


def haversine_distance(coord1, coord2):
    """
    Calculate the great-circle distance between two points on Earth using Haversine formula.
    
    Args:
        coord1 (tuple): (latitude, longitude) of first point
        coord2 (tuple): (latitude, longitude) of second point
    
    Returns:
        float: Distance in kilometers
    
    The Haversine formula is used to calculate the shortest distance between two points
    on a sphere (Earth) given their latitude and longitude coordinates.
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    # Haversine formula
    a = math.sin(delta_lat / 2) ** 2 + \
        math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    # Earth's radius in kilometers
    earth_radius = 6371.0
    
    return earth_radius * c


def straight_line_heuristic(current_station, goal_station):
    # Get coordinates for both stations
    current_coord = STATION_COORDINATES.get(current_station.name)
    goal_coord = STATION_COORDINATES.get(goal_station.name)
    
    # If coordinates not available, return 0 (still admissible but less informed)
    if not current_coord or not goal_coord:
        return 0.0
    
    # Calculate straight-line distance in kilometers
    distance_km = haversine_distance(current_coord, goal_coord)
    
    # Assume maximum average speed of 60 km/h for MRT
    # (Conservative estimate ensures admissibility)
    avg_speed_kmh = 60.0
    
    # Convert to seconds: (distance / speed) * 3600
    estimated_time_seconds = (distance_km / avg_speed_kmh) * 3600.0
    
    return estimated_time_seconds


def zero_heuristic(current_station, goal_station):
    """
    Zero heuristic (always returns 0).
    Used to convert A* into Uniform Cost Search for testing.
    
    Args:
        current_station (Station): Current station
        goal_station (Station): Goal station
    
    Returns:
        float: 0.0
    """
    return 0.0

def time_based_heuristic(station_from, station_to, transfer_dict, default_travel_time=120):
    # Minimum estimated travel: straight-line assumption in number of stations
    station_distance = station_from.distance_to(station_to)  # precomputed or 1 per station
    h = station_distance * default_travel_time

    # Add minimal transfer penalty if no common lines
    if set(station_from.lines).isdisjoint(station_to.lines):
        for line_from in station_from.lines:
            for line_to in station_to.lines:
                key = (station_from.name, station_from.name, line_from, line_to)
                if key in transfer_dict:
                    h += transfer_dict[key].transfer_time_seconds
                    break
    return h

def validate_heuristic(mrt_network, start_name, goal_name):
    """
    Validate that the heuristic is admissible by checking against actual path costs.
    
    Args:
        mrt_network (dict): Network of Station objects
        start_name (str): Starting station name
        goal_name (str): Goal station name
    
    Returns:
        dict: Validation results
    """
    if start_name not in mrt_network or goal_name not in mrt_network:
        return {"error": "Station not found"}
    
    start_station = mrt_network[start_name]
    goal_station = mrt_network[goal_name]
    
    # Calculate heuristic estimate
    h_estimate = straight_line_heuristic(start_station, goal_station)
    
    # Get coordinates
    start_coord = STATION_COORDINATES.get(start_name)
    goal_coord = STATION_COORDINATES.get(goal_name)
    
    if not start_coord or not goal_coord:
        return {"error": "Coordinates not available"}
    
    distance_km = haversine_distance(start_coord, goal_coord)
    
    return {
        "start": start_name,
        "goal": goal_name,
        "heuristic_estimate_seconds": h_estimate,
        "heuristic_estimate_minutes": h_estimate / 60.0,
        "straight_line_distance_km": distance_km,
        "is_admissible": "Unknown (requires actual path cost to verify)"
    }

# To calculate total time post path find (BFS & DFS)
def calculate_path_time(path, mrt_network, transfer_dict, default_travel_time=120):
    """
    Estimate travel time along a path in seconds.

    Args:
        path (list[str]): List of station names in order.
        mrt_network (dict[str, Station]): Network graph.
        transfer_dict (dict): Transfer timings (key: (station, station, line_from, line_to)).
        default_travel_time (int): Time between stations if unknown.

    Returns:
        total_time (int): Total time in seconds including transfers.
        transfer_count (int): Number of transfers encountered.
    """
    total_time = 0
    transfer_count = 0

    for i in range(len(path)-1):
        curr = mrt_network[path[i]]
        next_station = path[i+1]
        next_obj = mrt_network[next_station]

        # Travel time = assume fixed or stored in Station connections
        travel_time = curr.get_travel_time_to(next_obj) or default_travel_time
        total_time += travel_time

        # Check for line change to add transfer time
        lines_curr = curr.lines
        lines_next = next_obj.lines
        common_lines = set(lines_curr).intersection(lines_next)

        if not common_lines:
            # Different lines → find transfer
            for line_from in lines_curr:
                for line_to in lines_next:
                    key = (curr.name, curr.name, line_from, line_to)
                    if key in transfer_dict:
                        total_time += transfer_dict[key].transfer_time_seconds
                        transfer_count += 1
                        break

    return total_time, transfer_count

# Heuristic selection for experiments
HEURISTIC_FUNCTIONS = {
    "straight_line": straight_line_heuristic,
    "zero": zero_heuristic,
}