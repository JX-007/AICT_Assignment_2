def build_connections(line, stations_csv):
    stations = [s.strip() for s in stations_csv.split(",") if s.strip()]
    rows = []
    for a, b in zip(stations, stations[1:]):
        rows.append((line, a, b))
        rows.append((line, b, a))
    return rows

def main():
    line_code = input("Enter line code: ").strip().upper()
    stations = []
    while True:
        station_input = input("Enter station (or 'quit' to finish): ").strip()
        if station_input.lower() == "quit":
            break
        stations.append(station_input)
    
    if stations:
        rows = build_connections(line_code, ",".join(stations))
        print(f"\nGenerated {len(rows)} rows:")
        for row in rows:
            print(f"{row[0]},{row[1]},{row[2]}")

if __name__ == "__main__":
    main()