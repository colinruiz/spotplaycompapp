import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

CLIENT_ID = "0eb27e7c8598493fba46f54e10550e4f"
CLIENT_SECRET = "c520c87edc224b069f8ef996a5287642"
REDIRECT_URI = "http://127.0.0.1:8000/spotify/redirect"

def getUserPlaylists():
    try:
        os.remove(".cache")
    except:
        ()

    # scopes for auth_manager
    scope = "user-read-playback-state app-remote-control streaming user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, scope=scope, redirect_uri=REDIRECT_URI))
    #sp = spotipy.Spotify(auth_manager=SpotifyOAuth('f8a3f82ba99d46a694d89bc1cdc1cb09', '0dcbdb4f9fd0496683a16c01c93a9377', scope=scope, redirect_uri="http://127.0.0.1:8000/spotify/redirect"))
    total = sp.current_user_playlists()['total']
    print(type(total))
    playlists = []
    for i in range((total//50)+1):
        playlists+=sp.current_user_playlists(limit=50, offset=50*i)["items"]
    
    id_name = []
    for i in range(len(playlists)):
        id_name = (playlists[i]["id"], playlists[i]["name"])
    return id_name
        
        
print(getUserPlaylists())