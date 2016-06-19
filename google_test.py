from utils import get_api_key, points2distance
import math
import googlemaps

from googleplaces import GooglePlaces, types, lang

def get_centre_lat_long(ll1,ll2):
	lats = [ll1['lat'],ll2['lat']]
	lngs = [ll1['lng'],ll2['lng']]

	rad = (abs(max(lats)-min(lats))**2 + abs(max(lngs)-min(lngs))**2)**.5

	cen = {
		'lat': min(lats) + abs(max(lats)-min(lats))/2.,
		'lng': min(lngs) + abs(max(lngs)-min(lngs))/2.,
	}

	return cen, rad



def main(api_key):
	# Set up gmaps object with API key
	gmaps = googlemaps.Client(key=api_key)

	# use example start and end point
	start = gmaps.geocode('The Anchor, 34 Park St, Southwark, London SE1 9EF')
	print start
	end = gmaps.geocode("Southwark Brewing Company")
	print end

	print "The Anchor, 34 Park St, Southwark, London SE1 9EF" , start[0]['geometry']['location']
	print "Southwark Brewing Company" , end[0]['geometry']['location']

	##Get centre of latitude and longditude
	c_cen, c_rad = get_centre_lat_long(
		start[0]['geometry']['location'],
		end[0]['geometry']['location']
		)
	
	print "centre coord", c_cen
	print "centre radius", c_rad

	print 'calculated centre'
	print gmaps.reverse_geocode((c_cen['lat'],c_cen['lng']))

	##Search for places with radius rad (converted to metres)
	places = GooglePlaces(api_key)

	# You may prefer to use the text_search API, instead.
	print "radius metres", points2distance(
		[c_cen['lat'],c_cen['lng']],
		[start[0]['geometry']['location']['lat'],start[0]['geometry']['location']['lng']]
		)
	
	#nearby = places.radar_search(
    #    	lat_lng=c_cen,
    #    	keyword='beer',
     #   	radius=20000)


if __name__ == '__main__':
	api_key = get_api_key()
	main(api_key)



# Look up an address with reverse geocoding
#reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))


# Request directions via public transit
#now = datetime.now()
#directions_result = gmaps.directions("Sydney Town Hall",
#                                     "Parramatta, NSW",
#                                     mode="transit",
#                                    departure_time=now)