import unittest

class Calculator(object):
 
    def add(self, x, y):
        return x+y
 
class TddInPythonExample(unittest.TestCase):
 
    def test_calculator_add_method_returns_correct_result(self):
        calc = Calculator()
        result = calc.add(2,2)
        self.assertEqual(4, result)

class TestWaypointCalculator(unittest.TestCase):

	distance_matrix = [
	[1,5,5,5],
	[5,1,5,5]
	[5,5,1,5],
	[5,5,5,1]]

	def test_waypoint_object_picks_top_X_places(self):
		wpoints = waypoints()
		result = wpoints.pickTopX(5)
		self.assertEqual(,result)

	def test_get_ids_of_order_of_places(self):