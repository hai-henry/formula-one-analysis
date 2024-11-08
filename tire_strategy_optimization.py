import fastf1
import pandas as pd

fastf1.Cache.enable_cache("formula-one-analysis/cache")  # Enable caching for FastF1


# Load session (e.g., FP1, Race, Qualifying)
def load_race_data(year, grand_prix, session):
    session = fastf1.get_session(year, grand_prix, session)
    session.load()  # Loads session data (e.g., Telemetry, laps, etc.)
    return session


# Taking driver data
def extract_driver_data(session, driver_code):
    # Filter lap data for specified driver
    laps = session.laps.pick_driver(driver_code)

    driver_data = laps[["LapNumber", "LapTime", "Compound"]].copy()  # Select columns

    # Convert LapTime to seconds for calculations
    driver_data["LapTime_sec"] = driver_data["LapTime"].dt.total_seconds()

    # Format LapTime as MM:SS.sss
    driver_data["LapTime_str"] = driver_data["LapTime"].apply(
        lambda x: f"{int(x.total_seconds() // 60):02}:{int(x.total_seconds() % 60):02}.{int(x.microseconds / 1000):03}"
    )

    # Drop rows with missing lap times
    driver_data.dropna(subset=["LapTime_sec"], inplace=True)

    # Create column to indicate pit stops
    driver_data["PitStop"] = driver_data["Compound"].shift() != driver_data["Compound"]

    return driver_data


def main():
    session = load_race_data(2024, "Monza", "Race")  # Load session

    driver_data = extract_driver_data(session, "LEC")

    print(
        driver_data[["LapNumber", "LapTime_str", "LapTime_sec", "Compound", "PitStop"]]
    )


if __name__ == "__main__":
    main()
