from utils.utils import get_api_key, haversine, get_centre_lat_long
from utils.utils import get_lat_lng, distance_array, calculate_distances
import googlemaps

def get_nearby_places(gmaps,centre,radius,radius_factor,keywords):
	nearby = gmaps.places_radar(
		(centre['lat'], centre['lng']),
		radius=radius*radius_factor,
		keyword=keywords
		)

def filter_by_rating(gmaps,places_json,n_places):
	place_info = map(lambda x: gmaps.place(x['place_id']),places_json['results'])
	place_names = map(lambda x: x['result']['formatted_address'],place_info)
	place_rating = map(lambda x: x['result']['rating'] if 'rating' in x['result'] else 0,place_info)
	
	sorted_places = sorted(
			zip(place_names,place_rating),
			key=lambda x: x[1],
			reverse=True
			)
	return map(lambda x: x[0],sorted_places[:n_places+1])


def main(api_key):
	# Set up gmaps object with API key
	gmaps = googlemaps.Client(key=api_key)

	## Get global variables
	start_string = 'The Anchor, 34 Park St, Southwark, London SE1 9EF'
	end_string = 'Southwark Brewing Company'
	n_places = 2
	radius_factor = 1
	keywords = ['bar','beer']
	mode="bicycling"

	## Get location info on start and end points
	start = get_lat_lng(gmaps,start_string)
	end = get_lat_lng(gmaps,end_string)

	print start_string , start
	print end_string , end

	##Find centre and radius
	c_cen = get_centre_lat_long(start,end)
	radius = haversine(c_cen['lat'],c_cen['lng'],start['lat'],start['lng'])*1000
	print "centre coord", c_cen
	print "radius metres", radius
	
	
	##Get nearby places
	nearby = get_nearby_places(gmaps,c_cen,radius,radius_factor,keywords)

	###get places by rating
	top_places = filter_by_rating(gmaps,nearby,n_places)

	final_directions = gmaps.directions(
			start,
        	end,
        	mode=mode,
        	waypoints=top_places
        	)

	print final_directions



if __name__ == '__main__':
	api_key = get_api_key()
	main(api_key)