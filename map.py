"""Module that converts NASA facility lat/long data into a Google Earth-compatible KML file"""

import requests
import simplekml

API_ENDPOINT="https://data.nasa.gov/resource/gvk9-iz74.json"


def get_facility_list(endpoint: str) -> list:
    """
    Get the list of NASA facilities from NASA open dataset API
    """
    response = requests.get(endpoint,timeout=10)

    if response.status_code == 200:
        data = response.json()
        return data

    return f"Error: {response.status_code} - {response.text}"


def get_lat_long(facility: dict) -> tuple:
    """
    Get the latitude and longitude of a facility
    """
    return facility['location']['latitude'], facility['location']['longitude']


def build_kml(facility_list: list) -> None:
    """
    Builds a Google Earth-compatible KML file from a list of NASA facilities
    """

    kml = simplekml.Kml()

    for facility in facility_list:
        lat, long = get_lat_long(facility)
        kml.newpoint(name=facility["center"], coords=[(long, lat)])

    kml.save("coordinates.kml")


if __name__ == "__main__":
    facilities = get_facility_list(API_ENDPOINT)

    build_kml(facilities)
