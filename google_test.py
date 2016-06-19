from utils import get_api_key
import googlemaps

# Set up gmaps object with API key
gmaps = googlemaps.Client(key=get_api_key())


# Geocoding and address
geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

print geocode_result


# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# Request directions via public transit
#now = datetime.now()
#directions_result = gmaps.directions("Sydney Town Hall",
#                                     "Parramatta, NSW",
 #                                    mode="transit",
 #                                    departure_time=now)