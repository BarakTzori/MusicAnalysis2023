import numpy as np

# math aggregation functions over track and audio feature data

def getDanceability(audio_features):
    values = [d['danceability'] for d in filter(None, audio_features)]
    return dict(
            mean = np.mean(values),
            std = np.std(values))

def getAcousticness(audio_features):
    values = [d['acousticness'] for d in filter(None, audio_features)]
    return dict(
            mean = np.mean(values),
            std = np.std(values))

def getEnergy(audio_features):
    values = [d['energy'] for d in filter(None, audio_features)]
    return dict(
            mean = np.mean(values),
            std = np.std(values))

def getInstrumentalness(audio_features):
    values = [d['instrumentalness'] for d in filter(None, audio_features)]
    return dict(
            mean = np.mean(values),
            std = np.std(values))

def getLoudness(audio_features):
    values = [d['loudness'] for d in filter(None, audio_features)]
    return dict(
            mean = np.mean(values),
            std = np.std(values))

def getValence(audio_features):
    values = [d['valence'] for d in filter(None, audio_features)]
    return dict(
            mean = np.mean(values),
            std = np.std(values))
