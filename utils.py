def get_api_key():
	with open('api_key','r') as f:
		return f.read()