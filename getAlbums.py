#This file should take in our raw csv and produce a new csv will contain an album per row
# take the spotify track id from the raw csv
# call the get multiple tracks endpoint
# parse out album ids of each track
# call get multiple albums endpoint with ids
# create list of track ids from each album object returned
# write album name, release date, popularity, genres, artist names as list, album id

import requests

# get spotify auth token
URL = "https://accounts.spotify.com/api/token"
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
body = {
    'grant_type': 'client_credentials',
    'client_id': 'da0dd41dcd9042e99a92d3cef6579ca9',
    'client_secret': '47f0b0ffe059420fae7734bcbc8618f7'}

response = requests.post(url=URL, headers=headers, data=body)
access_token = response.json()['access_token']

# get track info by id
headers = {'Authorization': f'Bearer {access_token}'}
URL = 'https://api.spotify.com/v1/tracks/0Lf9AIOPZqprp67xBWbTG1'

response = requests.get(url=URL, headers=headers)
print(response.json()
print(response.json()['album']['id'])
