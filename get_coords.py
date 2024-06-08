import geopy
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time
import argparse

# Initialize Nominatim API with a proper user-agent
geolocator = Nominatim(user_agent="myemail@myemail.com", timeout=10)

# Set up argument parser
parser = argparse.ArgumentParser(description='Get coordinates for a list of locations.')
parser.add_argument('locations_file', type=str, help='Path to the file containing the list of locations')

# Parse arguments
args = parser.parse_args()

# Read the list of locations from the specified file
with open(args.locations_file, 'r') as file:
    locations = file.readlines()

# Function to get coordinates from Nominatim API
def get_coordinates(location, retries=3):
    try:
        location = location.strip()
        loc = geolocator.geocode(location)
        if loc:
            return f"{location}: {loc.latitude}, {loc.longitude}"
        else:
            return f"{location}: Not Found"
    except GeocoderTimedOut:
        if retries > 0:
            time.sleep(2)  # Wait before retrying
            return get_coordinates(location, retries - 1)
        return f"{location}: Error - Geocoder timed out"
    except GeocoderServiceError as e:
        if retries > 0:
            time.sleep(2)  # Wait before retrying
            return get_coordinates(location, retries - 1)
        return f"{location}: Error - {str(e)}"

# Iterate over each location and get coordinates
results = []
for location in locations:
    result = get_coordinates(location)
    results.append(result)
    print(result)
    # Sleep to respect Nominatim's usage policy
    time.sleep(1)

# Optionally, write the results to a file
with open('coordinates_output.txt', 'w') as output_file:
    for result in results:
        output_file.write(result + '\n')
