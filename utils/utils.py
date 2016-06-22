from math import radians, cos, sin, asin, sqrt
from itertools import combinations

def get_api_key():
	with open('api_key','r') as f:
		return f.read()

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def get_centre_lat_long(ll1,ll2):
  lats = [ll1['lat'],ll2['lat']]
  lngs = [ll1['lng'],ll2['lng']]

  cen = {
    'lat': min(lats) + abs(max(lats)-min(lats))/2.,
    'lng': min(lngs) + abs(max(lngs)-min(lngs))/2.,
  }

  return cen


def get_lat_lng(gmaps,place_text):
  return gmaps.geocode(place_text)[0]['geometry']['location']


def distance_array(dist_matrix,value='distance'):
  op = []
  for row in dist_matrix['rows']:
    #pass
    op.append(map(lambda x: x[value]['value'],row['elements']))
  #return dist_matrix
  return op


def calculate_distances(gmaps,start,end,place_names,n_places):
  op = []
  place_combs = combinations(place_names,n_places)
  for places in place_combs:
    routes = gmaps.directions(
      start,
          end,
          waypoints=list(places),
          optimize_waypoints=True
          )
    for route in routes:
      op.append([list(places), sum(map(lambda x: x['distance']['value'],route['legs']))])
  return op