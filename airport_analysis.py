import pandas as pd
import numpy as np


def load_data():
    """Load the required datasets from the nycflights13 repo"""
    airports_url = "https://raw.githubusercontent.com/hadley/nycflights13/master/data-raw/airports.csv"
    weather_url = "https://raw.githubusercontent.com/hadley/nycflights13/master/data-raw/weather.csv"

    airports = pd.read_csv(airports_url)
    weather = pd.read_csv(weather_url)

    # Convert time_hour to datetime
    weather['time_hour'] = pd.to_datetime(weather['time_hour'])

    return airports, weather


def find_northernmost_airport(airports):
    """Find the northernmost airport in the US"""
    # Filter US airports using timezone (since country column is missing)
    us_timezones = ['America/New_York', 'America/Chicago',
                    'America/Denver', 'America/Los_Angeles',
                    'America/Anchorage', 'Pacific/Honolulu']

    us_airports = airports[airports['tzone'].isin(us_timezones)].copy()
    northernmost = us_airports.sort_values('lat', ascending=False).head(5)
    return northernmost[['name', 'lat', 'lon', 'tzone']]


def find_easternmost_airport(airports):
    """Find the easternmost airport in the US"""
    # Filter US airports using timezone
    us_timezones = ['America/New_York', 'America/Chicago',
                    'America/Denver', 'America/Los_Angeles',
                    'America/Anchorage', 'Pacific/Honolulu']

    us_airports = airports[airports['tzone'].isin(us_timezones)].copy()

    # Create easternness measure (accounts for date line)
    us_airports['easternness'] = us_airports['lon'].apply(
        lambda x: (360 + x) if x < -120 else -x
    )
    easternmost = us_airports.sort_values('easternness', ascending=False).head(5)
    return easternmost[['name', 'lon', 'easternness', 'tzone']]


def find_windiest_ny_airport(weather):
    """Find which NY area airport had the windiest weather on Feb 12, 2013"""
    # Filter for the specific date
    feb12 = weather[weather['time_hour'].dt.date == pd.to_datetime('2013-02-12').date()]

    # Get max wind speed by origin
    windiest = feb12.groupby('origin')['wind_speed'].max().sort_values(ascending=False)
    return windiest


def main():
    print("Loading data...")
    try:
        airports, weather = load_data()

        print("\nFirst 3 airport records:")
        print(airports.head(3))

        print("\nTop 5 Northernmost airports in US:")
        northernmost = find_northernmost_airport(airports)
        print(northernmost.to_string(index=False))

        print("\nTop 5 Easternmost airports in US:")
        easternmost = find_easternmost_airport(airports)
        print(easternmost.to_string(index=False))

        print("\nWind speeds at NY area airports on Feb 12, 2013:")
        windiest = find_windiest_ny_airport(weather)
        print(windiest.to_string())

    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        if 'airports' in locals():
            print("\nDebugging info - Airport columns:", airports.columns.tolist())
            print("Sample timezone values:", airports['tzone'].unique()[:5])


if __name__ == "__main__":
    main()