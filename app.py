from flask import Flask, render_template, request
from utils.crawl_object import BeerCrawler
from utils.utils import get_api_key
import json

app = Flask(__name__)

radius_factor = 1
keywords = ['bar','beer']
api_key = get_api_key()

@app.route('/')
def main():

	start_string = "The Anchor, 34 Park St, Southwark, London SE1 9EF"
	end_string = "Southwark Brewing Company"
	
	return render_template(
		'index.html',
		init_start=start_string,
		init_end=end_string,
		api_key=api_key
		)


@app.route('/directions')
def signUp():

	_start = request.args['start']
	_end = request.args['end']
	_travel = request.args['travel']
	_stops = request.args['stops']

	bc = BeerCrawler(
		start_string=_start,
		end_string=_end,
		n_places=int(_stops),
		radius_factor=radius_factor,
		keywords=keywords,
		mode=_travel,
		api_key=api_key
		)

	bc.calculateCrawl()
	
	print bc.directions

	return json.dumps({'directions':bc.directions})


if __name__ == "__main__":
	app.run()