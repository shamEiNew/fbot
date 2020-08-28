import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
from os import environ

def configure():
    cs_id = environ['CLIENT_ID']
    cs_secret = environ['CLIENT_SECRET']

    client_credentials_manager = SpotifyClientCredentials(client_id=cs_id, client_secret=cs_secret)
    return spotipy.Spotify(client_credentials_manager = client_credentials_manager)

def song_pub(search_input):
    sp = configure()
    results = sp.search(q=search_input.strip().replace(' ','%20'), type='track', market='US' and 'IN',limit = 50)
     #Replace any space with '%20' or '+'
    print(search_input.strip().replace(' ','%20'))
    songs = results['tracks']['items']     #This is list.
    
    songs_f = {}                         #Definig dict for our list of songs with names and links.
    for i in range(0, len(songs)):
        songs_f[songs[i]['name']]=songs[i]['external_urls']['spotify']
    print(songs_f)
    return random.choice(list(songs_f.values()))
