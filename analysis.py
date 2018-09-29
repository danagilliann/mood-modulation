import csv
import requests
import json


def is_musician(is_string):
	if is_string.lower() == "yes":
		return True
	else:
		return False

'''
[{
	"artist": "artist"
	"track": "track"
	"is_musician": true	
}]
'''
def parse_csv():
	name = "sample.csv"
	result = []

	with open(name, newline="") as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')

		for row in csvreader:
			new_dict = {}
			new_dict["artist"] = row[3]
			new_dict["track"] = row[1]
			new_dict["is_musician"] = is_musician(row[2])

			result.append(new_dict)

	return result

def is_artist_in(artist_array, artist):
	for a_dict in artist_array:
		if a_dict.get("name") == artist:
			return True
	return False

def get_track_id(track_name, artist_name, OAUTH):
	track_name = track_name.replace(" ", "%20")
	url = "https://api.spotify.com/v1/search?q=" + track_name + "&type=track"
	bearer = "Bearer " + OAUTH 
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": bearer
	}

	req = requests.get(url, headers=headers)
	req = json.loads(req.text)

	req_items = req.get("tracks").get("items")

	# print("req", req.get("tracks"))

	for req_item in req_items:
		if req_item.get("artists") != None and is_artist_in(req_item.get("artists"), artist_name):
			return req_item.get("id")

def get_features(spotify_id, OAUTH):
	url = "https://api.spotify.com/v1/audio-features/" + spotify_id
	bearer = "Bearer " + OAUTH 
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
		"Authorization": bearer
	}

	req = requests.get(url, headers=headers)
	req = json.loads(req.text)

	print(req)

def get_audio_features(csv_results):
	OAUTH = "BQDOlf_s7IAA9TFBQmoV9ar5Sf70EDH4sEM6pJsjTpwSuoVcdA4ac5A65p3rhGb3nSNKTkK-tzl93tNjTQkXTR9jx5PUmDI-BtLKSfQiH4GOaR95UB-EmAscj5pnCH93FTA3qnMf2goGw5e0QteOoWOufCXcyoJbSG3tckF8EJpqV27u4X0j0URacgxv3e9ipFw0Jmm7wjWj0tfYe9xRgeAwXW3f2jUmcXGkKp7DtU0nzfrSVn4PyGAA42khPDTXEEhKqQw4qvEjcjO5Vrhu"
	# items[0].id

	for item in csv_results:
		track = item.get("track")
		artist = item.get("artist")

		spotify_id = get_track_id(track, artist, OAUTH)

		if spotify_id != None:
			get_features(spotify_id, OAUTH)


def main():
	csv_results = parse_csv()
	get_audio_features(csv_results)

main()
