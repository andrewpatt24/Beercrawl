from utils import get_api_key, haversine, get_centre_lat_long
from utils import get_lat_lng, distance_array, calculate_distances
import googlemaps

class BeerCrawler:
	"""
	BeerCrawler class to get a beer crawl direction set
	"""
	def __init__(self,start_string,end_string,n_places,radius_factor,keywords,mode,api_key):
		#Intitialise the googlemaps client
		self.gmaps = googlemaps.Client(key=api_key)

		#add functions that are being used to the class in case they need using
		self.haversine = haversine
		self.get_centre_lat_long = get_centre_lat_long
		self.get_lat_lng = get_lat_lng
		self.distance_array = distance_array
		self.calculate_distances = calculate_distances

		##assign initial variables
		self.start_string = start_string
		self.end_string = end_string
		self.n_places = n_places
		self.radius_factor = radius_factor
		self.keywords = keywords
		self.mode=mode
		self.api_key = api_key

	def getLatLngs(self):
		"""
		Get Latitiude and longditude of start and finish
		"""
		self.start = self.get_lat_lng(self.gmaps,self.start_string)
		self.end = self.get_lat_lng(self.gmaps,self.end_string)

	def findCentre(self):
		"""
		Find central point between start and finish
		"""
		self.centre = self.get_centre_lat_long(self.start,self.end)

	def calcRadius(self):
		"""
		Calculate Radius
		"""
		self.radius = self.haversine(
			self.centre['lat'],
			self.centre['lng'],
			self.start['lat'],
			self.start['lng']
			)*1000

	def getNearbyPlaces(self):
		"""
		Get nearby places given pre-calculated Radius and centre
		"""
		self.nearby = self.gmaps.places_radar(
			(self.centre['lat'], self.centre['lng']),
			radius=self.radius*self.radius_factor,
			keyword=self.keywords
			)

		self.place_ids = map(lambda x: x['place_id'],self.nearby['results'])
		self.place_info = map(lambda x: self.gmaps.place(x),self.place_ids)
		self.place_names = map(lambda x: x['result']['formatted_address'],self.place_info)

	def calcDistances(self):
		"""
		Use calculate distances function to calcualte distances between all places
		"""
		self.distances = self.calculate_distances(
			self.gmaps,
			self.start,
			self.end,
			self.place_names,
			self.n_places
			)

	def getMinRoute(self):
		"""
		Get directions for route with minimum distance
		"""
		self.min_dist = min([x[1] for x in self.distances])
		self.final_waypoints = [x for x in self.distances if x[1]==self.min_dist][0][0]

		self.directions = self.gmaps.directions(
				self.start,
				self.end,
				mode=self.mode,
				waypoints=self.final_waypoints
				)

	def calculateCrawl(self):
		"""
		Wrap up function to calcualte crawl
		"""
		self.getLatLngs()
		self.findCentre()
		self.calcRadius()
		self.getNearbyPlaces()
		self.calcDistances()
		self.getMinRoute()



if __name__ == '__main__':
	start_string = 'The Anchor, 34 Park St, Southwark, London SE1 9EF'
	end_string = 'Southwark Brewing Company'
	n_places = 2
	radius_factor = 1
	keywords = ['bar','beer']
	mode="bicycling"

	api_key = get_api_key()
	bc = BeerCrawler(
		start_string=start_string,
		end_string=end_string,
		n_places=n_places,
		radius_factor=radius_factor,
		keywords=keywords,
		mode=mode,
		api_key=api_key)

	bc.calculateCrawl()
	
	print bc.directions