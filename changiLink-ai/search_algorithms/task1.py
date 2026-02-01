import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from mrtNetwork import load_mrt_connections, build_mrt_network, load_future_mrt_connections

from bfs import breadth_first_search
from dfs import depth_first_search
from gbfs import gbfs
from astar import a_star

from Classes.transfer import load_transfer_timings
from Classes.station import get_lines_to

# Path to your CSV
transfer_csv_path = "AICT_Assignment_2\changiLink-ai\Data\MRT transfer timing.csv"

# Load transfer timings
TRANSFER_TIMINGS_DICT, TRANSFER_TIMINGS_LIST = load_transfer_timings(transfer_csv_path)


# ---------------- CONFIG ----------------

CURRENT_PAIRS = [
    ("Changi Airport", "City Hall"),
    ("Changi Airport", "Orchard"),
    ("Changi Airport", "Gardens by the Bay"),
    ("Changi Airport", "HarbourFront"),
    ("Changi Airport", "Jurong East")
]

FUTURE_PAIRS = [
    ("Paya Lebar", "T5 Interchange"),
    ("HarbourFront", "T5 Interchange"),
    ("Bishan", "T5 Interchange"),
    ("Tampines", "T5 Interchange"),
    ("Bukit Gombak", "T5 Interchange")
]

ALGORITHMS = [
    ("BFS", breadth_first_search),
    ("DFS", depth_first_search),
    ("GBFS", gbfs),
    ("A*", a_star)
]

# -------- Calculate Edge Cost -------- #
def edge_cost(from_station, to_station, lines_traveled):
    """
    Calculate travel time for an edge including transfer penalty if changing lines.
    
    Args:
        from_station (Station): Starting station object
        to_station (Station): Destination station object
        lines_traveled (list[str]): Lines used along this edge (usually length 1 or 2)
    
    Returns:
        float: total travel time in minutes
    """
    # Base travel time between two stations (default)
    base_time = 2  # minutes

    # If a line change occurs along this edge
    if len(lines_traveled) > 1 and lines_traveled[0] != lines_traveled[1]:
        # Transfer happens at from_station
        key = (from_station.name, from_station.name, lines_traveled[0], lines_traveled[1])
        transfer = TRANSFER_TIMINGS_DICT.get(key)
        if transfer:
            base_time += transfer.transfer_time_minutes
        else:
            print(f"Transfer not found for {key}")

    return base_time

# ---------------- MAIN ----------------
def build_network(use_future):
    network_data = load_mrt_connections()

    if use_future:
        future_csv = os.path.join(PROJECT_ROOT, "Data", "future_mrt_connections.csv")
        network_data = load_future_mrt_connections(future_csv, network_data)

    return build_mrt_network(network_data)

import time

def run_tests(mrt_network, pairs):
    results = {}  # Store results
    for start, goal in pairs:
        print("\n" + "=" * 60)
        print(f"ROUTE: {start} → {goal}")

        results[(start, goal)] = {}  # Initialize dict for this OD pair

        for name, algo in ALGORITHMS:
            print("\n" + "-" * 40)
            print(f"{name}")

            start_time = time.perf_counter()       # Start timer
            path, expanded, memory = algo(mrt_network, start, goal)
            end_time = time.perf_counter()           # End timer
            runtime = end_time - start_time   # Calculate runtime in seconds

            if path:
                print("Path:", " → ".join(path))
                total_travel_time = 0
                for i in range(len(path)-1):
                    station_a = mrt_network[path[i]]
                    station_b = mrt_network[path[i+1]]

                    # Lines connecting these stations
                    lines = []
                    for conn, conn_lines in station_a.get_connections():
                        if conn.name == station_b.name:
                            lines = conn_lines
                            break

                    total_travel_time += edge_cost(station_a, station_b, lines)

                print(f"Total travel time: {total_travel_time:.2f} minutes")
            else:
                total_travel_time = None
                print("No path found")

            print(f"Nodes Expanded: {expanded}")
            print(f"Memory Used: {memory} bytes")
            print(f"Runtime: {runtime:.4f} seconds")

            # Save results
            results[(start, goal)][name] = {
                "path": path,
                "total_travel_time": total_travel_time,
                "nodes_expanded": expanded,
                "memory": memory,
                "runtime": runtime
            }

    return results

# ------- RESULT COMPARISON ------- #
import pandas as pd

def results_to_dataframe(results):
    rows = []
    for (start, goal), algo_data in results.items():
        for algo_name, metrics in algo_data.items():
            rows.append({
                "Start": start,
                "Goal": goal,
                "Algorithm": algo_name,
                "Total Travel Time (min)": metrics["total_travel_time"],
                "Nodes Expanded": metrics["nodes_expanded"],
                "Memory (bytes)": metrics["memory"],
                "Runtime (s)": metrics["runtime"]
            })
    df = pd.DataFrame(rows)
    return df
import matplotlib.pyplot as plt

def plot_runtime_comparison(df):
    for (start, goal), group in df.groupby(["Start", "Goal"]):
        plt.figure(figsize=(8,5))
        plt.bar(group["Algorithm"], group["Runtime (s)"], color='skyblue')
        plt.title(f"Runtime Comparison: {start} → {goal}")
        plt.ylabel("Time (s)")
        plt.xlabel("Algorithm")
        plt.show()

def plot_nodes_comparison(df):
    for (start, goal), group in df.groupby(["Start", "Goal"]):
        plt.figure(figsize=(8,5))
        plt.bar(group["Algorithm"], group["Nodes Expanded"], color='orange')
        plt.title(f"Nodes Expanded Comparison: {start} → {goal}")
        plt.ylabel("Nodes Expanded")
        plt.xlabel("Algorithm")
        plt.show()

def plot_travel_time_comparison(df):
    for (start, goal), group in df.groupby(["Start", "Goal"]):
        plt.figure(figsize=(8,5))
        plt.bar(group["Algorithm"], group["Total Travel Time (min)"], color='green')
        plt.title(f"Total Travel Time Comparison: {start} → {goal}")
        plt.ylabel("Minutes")
        plt.xlabel("Algorithm")
        plt.show()

# -------- GRAPH PLOTTING --------- #
import matplotlib.pyplot as plt

def plot_runtime_comparison(df):
    plt.figure(figsize=(10,6))
    for algo in df['Algorithm'].unique():
        subset = df[df['Algorithm'] == algo]
        plt.plot(subset['Goal'], subset['Runtime (s)'], marker='o', label=algo)
    plt.title("Algorithm Runtime Comparison")
    plt.xlabel("Destination Station")
    plt.ylabel("Runtime (s)")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_nodes_comparison(df):
    plt.figure(figsize=(10,6))
    for algo in df['Algorithm'].unique():
        subset = df[df['Algorithm'] == algo]
        plt.plot(subset['Goal'], subset['Nodes Expanded'], marker='o', label=algo)
    plt.title("Nodes Expanded Comparison")
    plt.xlabel("Destination Station")
    plt.ylabel("Nodes Expanded")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_travel_time_comparison(df):
    plt.figure(figsize=(10,6))
    for algo in df['Algorithm'].unique():
        subset = df[df['Algorithm'] == algo]
        plt.plot(subset['Goal'], subset['Total Travel Time (min)'], marker='o', label=algo)
    plt.title("Total Travel Time Comparison")
    plt.xlabel("Destination Station")
    plt.ylabel("Total Travel Time (min)")
    plt.legend()
    plt.grid(True)
    plt.show()

# ------------- MAIN -------------- #
if __name__ == "__main__":
    print("Select MRT Simulation Mode")
    print("1 - Current MRT Network")
    print("2 - Future MRT Network (with T5)")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        print("\nRunning CURRENT MRT simulation...")
        mrt_network = build_network(use_future=False)
        results = run_tests(mrt_network, CURRENT_PAIRS)
        df = results_to_dataframe(results)
        print(df)  # view results in table form

        # Plot graphs
        plot_runtime_comparison(df)
        plot_nodes_comparison(df)
        plot_travel_time_comparison(df)

    elif choice == "2":
        print("\nRunning FUTURE MRT simulation (with T5)...")
        mrt_network = build_network(use_future=True)
        results = run_tests(mrt_network, FUTURE_PAIRS)
        df = results_to_dataframe(results)
        print(df)  # view results in table form

        # Plot graphs
        plot_runtime_comparison(df)
        plot_nodes_comparison(df)
        plot_travel_time_comparison(df)

    else:
        print("Invalid choice. Please run again.")
