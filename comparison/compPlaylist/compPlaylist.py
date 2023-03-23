import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os

CLIENT_ID = "0eb27e7c8598493fba46f54e10550e4f"
CLIENT_SECRET = "c520c87edc224b069f8ef996a5287642"
REDIRECT_URI = "http://127.0.0.1:8000/spotify/redirect"

#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))
#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials('f8a3f82ba99d46a694d89bc1cdc1cb09', '0dcbdb4f9fd0496683a16c01c93a9377'))

# test playlist ids
id1='spotify:playlist:37i9dQZF1EQqlvxWrOgFZm'
id2='spotify:playlist:37i9dQZF1DX3LDIBRoaCDQ'


# compares two playlists
def comparePlaylists(playlist1_id, playlist2_id):
    # deletes the cache file so that there is no opportunity for the cache to mess up the authorization manager
    try:
        os.remove(".cache")
    except:
        ()
    
    # scopes for auth_manager
    scope = "user-read-playback-state app-remote-control streaming user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, scope=scope, redirect_uri=REDIRECT_URI))
    #sp = spotipy.Spotify(auth_manager=SpotifyOAuth('f8a3f82ba99d46a694d89bc1cdc1cb09', '0dcbdb4f9fd0496683a16c01c93a9377', scope=scope, redirect_uri="http://127.0.0.1:8000/spotify/redirect"))

    # counts the number of shared tracks
    count=0
    # gets playlist lengths
    length1=sp.playlist(playlist1_id)['tracks']['total']
    length2=sp.playlist(playlist2_id)['tracks']['total']
    # iterates through playlists and adds to a list to be compared
    list2 = []
    for k in range((length2//100)+1):
        playlist2=sp.playlist_tracks(playlist2_id, limit=100, offset=100*(k))['items']
        for a in playlist2:
            list2.append(a['track']['id'])
                
    list1 = []
    for i in range((length1//100)+1):
        playlist1=sp.playlist_tracks(playlist1_id, limit=100, offset=100*i)['items']
        for a in playlist1:
            list1.append(a['track']['id'])

    # finds the number of common tracks
    for i in list1:
        #print(i)
        if i in list2:
            count+=1
        
    return "The two playlists have "+str(round((count/(length1+length2-count))*100, 2))+"%"+' in common'
    
print(comparePlaylists(id1, id2))