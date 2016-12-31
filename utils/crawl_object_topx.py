from utils import get_api_key, haversine, get_centre_lat_long
from utils import get_lat_lng, distance_array, calculate_distances
import googlemaps

class BeerCrawler:
	"""
	BeerCrawler class to get a beer crawl direction set
	global class that holds functions by all BeerCrawler classes
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
			)['results']

		##Lets create a master dict in the object which has all the place info
		##we can then pull the day out after the fact instead of constantly adding terms
		for i in xrange(len(self.nearby)):
			self.nearby[i]['place_info'] = self.gmaps.place(self.nearby[i]['place_id'])

		##some ratings are missing - lets add them in as zero
		for i in xrange(len(self.nearby)):
			if 'rating' not in self.nearby[i]['place_info']['result'].keys():
				self.nearby[i]['place_info']['result']['rating'] = 0



class TopXBeerCrawler(BeerCrawler):
	def getTopXWaypoint(self,w=1):
		"""
		Gets tops X places by ratings
		"""
		return sorted(
				self.nearby,
				key=lambda x: x['place_info']['result']['rating']
			)[0:w]

	def getTopPlacesRoute(self):
		"""
		Finds top X places and calcualtes route
		"""
		self.final_waypoints = self.getTopXWaypoint(self.n_places)

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

	bc.calculateTopXCrawl()
	
	print bc.directions