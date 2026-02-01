import os
import sys
import time


PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from mrtNetwork import build_mrt_network

# ============================================================================
# DEPTH-FIRST SEARCH (DFS) ALGORITHM STEPS
# ============================================================================
# DFS explores deeply along one branch before backtracking. It's memory
# efficient but not optimal for pathfinding. Uses LIFO (stack) principle.
# ============================================================================

# STEP 1: Initialize Data Structures
def initialize_dfs():
    """
    STEP 1: Initialize DFS data structures
    - Create stack for nodes to explore (LIFO - Last In, First Out)
    - Create visited set to avoid revisiting nodes
    - Create came_from dict to track parent relationships
    """
    return [], set(), {}


# STEP 2: Push Start Node to Stack
def push_start_node(stack, start_station, came_from):
    """
    STEP 2: Add start station to stack
    - Push (station, line) tuple to stack
    - Mark start station as explored
    - Initialize came_from with None parent
    """
    start_key = (start_station, None)
    stack.append(start_key)
    came_from[start_key] = None
    return stack


# STEP 3: Main DFS Exploration Loop
def dfs_search(start_station, goal_station):
    """
    STEP 3: Main Depth-First Search Algorithm
    
    Process:
    a) Initialize stack, visited set, came_from dict
    b) Push start station to stack
    c) Loop while stack not empty (LIFO):
       - Pop top node from stack
       - If already visited, skip (avoid cycles)
       - Mark as visited
       - If goal reached, return success
       - Else, explore all unvisited neighbors
       - For each unvisited neighbor:
         * Push to stack
         * Record current as parent in came_from
         * Will be explored in LIFO order (most recent first)
    d) Return came_from dict for path reconstruction
    """
    # STEP 3a: Initialize data structures
    stack, visited, came_from = initialize_dfs()
    
    # STEP 3b: Push start station
    stack = push_start_node(stack, start_station, came_from)
    
    goal_key = None
    nodes_expanded = 0

    # STEP 3c: Main exploration loop
    while stack:
        current_station, current_line = stack.pop()  # Pop from end (LIFO)
        current_key = (current_station, current_line)
        
        # Skip if already visited (prevent cycles)
        if current_key in visited:
            continue
        
        visited.add(current_key)
        nodes_expanded += 1

        # Check if goal reached
        if current_station == goal_station:
            goal_key = current_key
            break

        # Explore neighbors
        neighbors = list(current_station.get_neighbors())
        # Reverse to maintain consistent exploration order (stack is LIFO)
        for next_station, lines in reversed(neighbors):
            next_line = current_line if current_line in lines else (lines[0] if lines else current_line)
            next_key = (next_station, next_line)
            
            # Only consider unvisited neighbors
            if next_key not in visited:
                # Push to stack (will be popped last due to LIFO)
                stack.append(next_key)
                
                # Record parent if first time seeing this node
                if next_key not in came_from:
                    came_from[next_key] = current_key

    # STEP 3d: Return came_from for path reconstruction
    return came_from, goal_key, nodes_expanded


# STEP 4: Backtracking (implicit in came_from tracking)
# Note: Backtracking happens naturally when we pop from stack
# and reach a dead end - we then pop an earlier node to explore
# alternative branches


# STEP 5: Path Reconstruction with Time Calculation
def reconstruct_path(came_from, end_key):
    """
    STEP 5: Reconstruct path from goal back to start
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


# STEP 6: Main Execution and Display Results
if __name__ == "__main__":
    mode_input = input("(Today or Future)Mode: ").strip().lower()
    mode = "Future" if mode_input == "future" else "Today"

    mrt_network = build_mrt_network(mode=mode)

    start_station_name = input("Enter start station: ").strip()
    start_station = mrt_network[start_station_name]
    goal_station_name = input("Enter goal station: ").strip()
    goal_station = mrt_network[goal_station_name]

    start_time = time.perf_counter()
    came_from, goal_key, nodes_expanded = dfs_search(start_station, goal_station)
    elapsed = time.perf_counter() - start_time

    path, total_time = reconstruct_path(came_from, goal_key)
    if path:
        print(" → ".join(path))
        print(f"Total time: {int(total_time)//3600}:{(int(total_time)%3600)//60:02d}:{int(total_time)%60:02d} (hh:mm:ss)")
        print(f"Path length: {len(path)}")
    else:
        print("No path found.")
    print(f"Nodes expanded: {nodes_expanded}")
    print(f"Runtime: {elapsed:.6f}s")

# Note: DFS explores deeply along one branch before backtracking.
# It's less efficient for pathfinding than A* or GBFS but is memory-friendly.