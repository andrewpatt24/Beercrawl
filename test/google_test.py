from utils import get_api_key, haversine, get_centre_lat_long
from utils import get_lat_lng, distance_array, calculate_distances
import googlemaps

class BeerCrawler:
    """BeerCrawler class to get a beer crawl direction set"""
    def __init__(self,api_key):
    	self.start_string = 'The Anchor, 34 Park St, Southwark, London SE1 9EF'
		self.end_string = 'Southwark Brewing Company'
		self.n_places = 2
		self.radius_factor = 1
		self.keywords = ['bar','beer']
		self.mode="bicycling"
		self.api_key = api_key
		self.gmaps = googlemaps.Client(key=api_key)


    def get_lat_lngs(self):
    	self.start = get_lat_lng(self.gmaps,self.start_string)
    	self.end = get_lat_lng(self.gmaps,self.end_string)

    def find_centre(self):
    	self.centre = get_centre_lat_long(self.start,self.end)

    def calculate_radius(self):
    	self.radius = haversine(
    		self.c_cen['lat'],
    		self.c_cen['lng'],
    		self.start['lat'],
    		self.start['lng']
    		)*1000

    def get_nearby_places(self):
    	##Get nearby places
		self.nearby = self.gmaps.places_radar(
			(self.c_cen['lat'], self.c_cen['lng']),
			radius=self.radius*self.radius_factor,
			keyword=self.keywords
			)

		self.place_ids = map(lambda x: x['place_id'],self.nearby['results'])
		self.place_info = map(lambda x: self.gmaps.place(x),self.place_ids)
		self.place_names = map(lambda x: x['result']['formatted_address'],self.place_info)

	def calculate_distances(self):
		self.distances = calculate_distances(
			self.gmaps,
			self.start,
			self.end,
			self.place_names,
			self.n_places
			)

	











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
	
	print "centre coord", c_cen

	# You may prefer to use the text_search API, instead.
	radius = haversine(c_cen['lat'],c_cen['lng'],start['lat'],start['lng'])*1000

	print "radius metres", radius
	
	##Get nearby places
	nearby = gmaps.places_radar(
		(c_cen['lat'], c_cen['lng']),
		radius=radius*radius_factor,
		keyword=keywords
		)

	###get info lists
	place_ids = map(lambda x: x['place_id'],nearby['results'])
	place_info = map(lambda x: gmaps.place(x),place_ids)
	place_names = map(lambda x: x['result']['formatted_address'],place_info)

	#calculate distances from combinations
	distances = calculate_distances(gmaps,start,end,place_names,n_places)

	#get min distance for waypoints
	min_dist = min([x[1] for x in distances])
	print min_dist
	final_waypoints = [x for x in distances if x[1]==min_dist]
	print final_waypoints
	print min_dist

	final_directions = gmaps.directions(
			start,
        	end,
        	mode=mode,
        	waypoints=final_waypoints[0][0]
        	)

	print final_directions



if __name__ == '__main__':
	api_key = get_api_key()
	main(api_key)