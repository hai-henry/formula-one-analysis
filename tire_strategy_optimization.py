import fastf1
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

fastf1.Cache.enable_cache("formula-one-analysis/cache")  # Enable caching for FastF1


# Load session (eg. FP1, Race, Qualifying)
def load_race_data(year, grand_prix, session):
    session = fastf1.get_session(year, grand_prix, session)
    session.load()  # Loads session data (eg. Telemetry, laps, etc.)
    return session


# Analyzing driver tire degradation
def analyze_tire_degradation(session, driver_code):
    laps = session.laps.pick_driver(driver_code)  # Get driver laps
    driver_laps = laps[["LapNumber", "LapTime", "Compound"]]  # Select columns

    # Convert Lap time to seconds
    driver_laps["LapTime"] = driver_laps["LapTime"].dt.total_seconds()

    # Drop rows with missing lap times
    driver_laps = driver_laps.dropna(subset=["LapTime"])

    # Create column to indicate pit stops
    driver_laps["PitStop"] = driver_laps["Compound"].shift() != driver_laps["Compound"]

    plt.figure(figsize=(12, 6))  # Figure size
    for compound, laps in driver_laps.groupby("Compound"):  # Group by tire compound
        plt.plot(laps["LapNumber"], laps["LapTime"], label=compound)  # Plot lap times

    pit_stops = driver_laps[driver_laps["PitStop"]]  # Get pit stops

    # Plot pit stops
    plt.scatter(
        pit_stops["LapNumber"],
        pit_stops["LapTime"],
        color="red",
        marker="x",
        s=100,
        label="Pit Stop",
    )

    # Plot
    plt.xlabel("Lap Number")
    plt.ylabel("Lap Time (s)")
    plt.legend()
    plt.title(f"Tire Degradation by Compound for {driver_code}")
    plt.show()


def main():
    session = load_race_data(2024, "Monza", "Race")  # Load session
    analyze_tire_degradation(session, "HAM")  # Analyze tire degradation for driver


if __name__ == "__main__":
    main()
