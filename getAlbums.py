#This file should take in our raw csv and produce a new csv will contain an album per row
# take the spotify track id from the raw csv
# call the get multiple tracks endpoint
# parse out album ids of each track
# call get multiple albums endpoint with ids
# create list of track ids from each album object returned
# write album name, release date, popularity, genres, artist names as list, album id

import requests
import pandas as pd
from collections import defaultdict

# get spotify auth token
def getSpotifyToken():
    URL = "https://accounts.spotify.com/api/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {
        'grant_type': 'client_credentials',
        'client_id': 'da0dd41dcd9042e99a92d3cef6579ca9',
        'client_secret': '47f0b0ffe059420fae7734bcbc8618f7'}

    response = requests.post(url=URL, headers=headers, data=body)
    return response.json()['access_token']

# read in the raw csv
def createPreliminaryAlbumDataCSV(access_token, output_file):
    filename = 'song_an_album.csv'
    raw_data = pd.read_csv(filename)

    album_data = pd.DataFrame()
    output_file = 'album_data.csv'

    # get list of album ids from tracks by calling get track on each song
    headers = {'Authorization': f'Bearer {access_token}'}
    URL = 'https://api.spotify.com/v1/tracks/'

    album_ids = []
    release_dates = []
    for track_id in raw_data['Spotify ID'].values:
        response = requests.get(url=f'{URL}{track_id}', headers=headers)
        album_ids.append(response.json()['album']['id'])
        release_dates.append(response.json()['album']['release_date'])
        print(response.json()['album']['name'])

    album_data['album_ids'] = album_ids
    album_data['release_date'] = release_dates
    album_data['date_added'] = raw_data['Added At']
    album_data['album_name'] = raw_data['Album Name']
    album_data.to_csv(output_file, encoding='utf-16', index=False)

def main():
    output_file = 'album_data.csv'

    access_token = getSpotifyToken()

    #once we've run this once the csv exists, so no need to run again
    # can rerun if starting with a different raw data file
    #createPreliminaryAlbumDataCSV(access_token, output_file)



if __name__ == "__main__":
    main()

