#This file should take in our raw csv and produce a new csv will contain an album per row
# take the spotify track id from the raw csv
# call the get multiple tracks endpoint
# parse out album ids of each track
# call get multiple albums endpoint with ids
# create list of track ids from each album object returned
# write album name, release date, popularity, genres, artist names as list, album id

import requests
import pandas as pd
import numpy as np
from collections import defaultdict

from aggregationFunctions import *

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
    album_data['artists_names'] = raw_data['Artist Name(s)']
    album_data['genres'] = raw_data['Genres']
    album_data.to_csv(output_file, header=True, encoding='utf-16', index=False)

# collect all the information possible by making a single get album call
# takes in the spotify id of the album
# should return an object that has a list of song ids, total album duration, popularity
def extractGeneralAlbumData(album_id, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    URL = f'https://api.spotify.com/v1/albums/{album_id}'

    response = requests.get(url=URL, headers=headers)

    track_ids = []
    duration = 0
    tracks = response.json()['tracks']['items']

    for track in tracks:
        track_ids.append(track['id'])
        duration = duration + track['duration_ms']

    return dict(
            track_ids = ','.join(track_ids),
            duration = duration,
            popularity = response.json()['popularity'])

# reads in the csv which has album ids, and generates the general album info, and overwrites the file
def collectAllAlbumTracks(filename, access_token):
    data = pd.read_csv(filename, encoding='utf-16')
    
    durations = []
    popularities = []
    track_ids = [] 
    for album_id in data['album_ids']:
        album_properties = extractGeneralAlbumData(album_id, access_token)
        durations.append(album_properties['duration'])
        popularities.append(album_properties['popularity'])
        track_ids.append(album_properties['track_ids'])

    data['duration'] = durations
    data['popularity'] = popularities
    data['track_ids'] = track_ids
    data.to_csv(filename, header=True, encoding='utf-16', index=False)

# calls get tracks and get audio features for all tracks passed in
# gathers meaningful metrics from the data
def aggregateTrackDataForAlbum(album_track_ids, access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    get_audio_features_url = f'https://api.spotify.com/v1/audio-features?ids={album_track_ids}'

    audio_features_response = requests.get(url=get_audio_features_url, headers=headers)

    audio_features = audio_features_response.json()['audio_features']

    danceability = getDanceability(audio_features)
    acousticness = getAcousticness(audio_features)
    energy = getEnergy(audio_features)
    loudness = getLoudness(audio_features)
    valence = getValence(audio_features)
    pct_major = getPctMajor(audio_features)

    return dict(
            danceability_min = danceability['minim'],
            danceability_max = danceability['maxim'],
            danceability_mean = danceability['mean'],
            danceability_std = danceability['std'],
            acousticness_min = acousticness['minim'],
            acousticness_max = acousticness['maxim'],
            acousticness_mean = acousticness['mean'],
            acousticness_std = acousticness['std'],
            energy_min = energy['minim'],
            energy_max = energy['maxim'],
            energy_mean = energy['mean'],
            energy_std = energy['std'],
            loudness_min = loudness['minim'],
            loudness_max = loudness['maxim'],
            loudness_mean = loudness['mean'],
            loudness_std = loudness['std'],
            valence_min = valence['minim'],
            valence_max = valence['maxim'],
            valence_mean = valence['mean'],
            valence_std = valence['std'],
            pct_major = pct_major)


# reads in the album csv, loops over each album, and gets all songs from each and performs deep level aggregation
def aggregateAllData(filename, access_token):
    data = pd.read_csv(filename, encoding='utf-16')

    danceability_mins = []
    danceability_maxs = []
    danceability_means = []
    danceability_stds = []
    acousticness_mins = []
    acousticness_maxs = []
    acousticness_means = []
    acousticness_stds = []
    energy_mins = []
    energy_maxs = []
    energy_means = []
    energy_stds = []
    loudness_mins = []
    loudness_maxs = []
    loudness_means = []
    loudness_stds = []
    valence_mins = []
    valence_maxs = []
    valence_means = []
    valence_stds = []
    pct_majors = []

    for index, row in data.iterrows():
        print(index, row['album_name'])
        vals = aggregateTrackDataForAlbum(row['track_ids'], access_token)
        danceability_mins.append(vals['danceability_min'])
        danceability_maxs.append(vals['danceability_max'])
        danceability_means.append(vals['danceability_mean'])
        danceability_stds.append(vals['danceability_std'])
        acousticness_mins.append(vals['acousticness_min'])
        acousticness_maxs.append(vals['acousticness_max'])
        acousticness_means.append(vals['acousticness_mean'])
        acousticness_stds.append(vals['acousticness_std'])
        energy_mins.append(vals['energy_min'])
        energy_maxs.append(vals['energy_max'])
        energy_means.append(vals['energy_mean'])
        energy_stds.append(vals['energy_std'])
        loudness_mins.append(vals['loudness_min'])
        loudness_maxs.append(vals['loudness_max'])
        loudness_means.append(vals['loudness_mean'])
        loudness_stds.append(vals['loudness_std'])
        valence_mins.append(vals['valence_min'])
        valence_maxs.append(vals['valence_max'])
        valence_means.append(vals['valence_mean'])
        valence_stds.append(vals['valence_std'])
        pct_majors.append(vals['pct_major'])


    data['danceability_min'] = danceability_mins
    data['danceability_max'] = danceability_maxs
    data['danceability_mean'] = danceability_means
    data['danceability_std'] = danceability_stds
    data['acousticness_min'] = acousticness_mins
    data['acousticness_max'] = acousticness_maxs
    data['acousticness_mean'] = acousticness_means
    data['acousticness_std'] = acousticness_stds
    data['energy_min'] = energy_mins
    data['energy_max'] = energy_maxs
    data['energy_mean'] = energy_means
    data['energy_std'] = energy_stds
    data['loudness_min'] = loudness_mins
    data['loudness_max'] = loudness_maxs
    data['loudness_mean'] = loudness_means
    data['loudness_std'] = loudness_stds
    data['valence_min'] = valence_mins
    data['valence_max'] = valence_maxs
    data['valence_mean'] = valence_means
    data['valence_std'] = valence_stds
    data['pct_major'] = pct_majors

    data.to_csv(filename, header=True, encoding='utf-16', index=False)

def combineManualCSV(filename, manual_csv_file):
    data = pd.read_csv(filename, encoding='utf-16')
    custom_data = pd.read_csv(manual_csv_file)

    data['overall_genre'] = custom_data['overall_genre']
    data['new'] = custom_data['new']
    data['revisited'] = custom_data['revisited']
    data['rating'] = custom_data['rating']

    data.to_csv(filename, header=True, encoding='utf-16', index=False)


def main():
    filename = 'album_data.csv'
    manual_csv_file = 'custom_data.csv'

    access_token = getSpotifyToken()

    #once we've run this once the csv exists, so no need to run again
    # can rerun if starting with a different raw data file
    #createPreliminaryAlbumDataCSV(access_token, filename)

    # put all album track ids into each column, so we can go in later and run aggregations
    #collectAllAlbumTracks(filename, access_token)

    # put together all deep level data
    aggregateAllData(filename, access_token)

    # add in additional manual data
    # needs to start in a separate csv for some encoding reasons
    combineManualCSV(filename, manual_csv_file)

if __name__ == "__main__":
    main()

