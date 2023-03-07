import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import credentials

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(credentials.CLIENT_ID, credentials.CLIENT_SECRET))
#spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials('f8a3f82ba99d46a694d89bc1cdc1cb09', '0dcbdb4f9fd0496683a16c01c93a9377'))

#print(results['artists'][0]['name'])

scope = "user-read-playback-state app-remote-control streaming user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(credentials.CLIENT_ID, credentials.CLIENT_SECRET, scope=scope, redirect_uri=credentials.REDIRECT_URI))
#sp = spotipy.Spotify(auth_manager=SpotifyOAuth('f8a3f82ba99d46a694d89bc1cdc1cb09', '0dcbdb4f9fd0496683a16c01c93a9377', scope=scope, redirect_uri="http://127.0.0.1:9000"))
id1='spotify:playlist:37i9dQZF1EQqlvxWrOgFZm'
id2='spotify:playlist:37i9dQZF1DX3LDIBRoaCDQ'




#print(folk_acoustic_mix['items'][0]['track']['artists'][0]['name']+": "+folk_acoustic_mix['items'][0]['track']['name'])
def comparePlaylists(playlist1_id, playlist2_id):
    count=0
    length1=sp.playlist(playlist1_id)['tracks']['total']
    length2=sp.playlist(playlist2_id)['tracks']['total']
    list2 = []
    for k in range((length2//100)):
        playlist2=sp.playlist_tracks(playlist2_id, limit=100, offset=100*k)['items']
        for a in playlist2:
            list2.append(a['track']['id'])
                
    list1 = []
    for i in range((length1//100)+1):
        playlist1=sp.playlist_tracks(playlist1_id, limit=100, offset=100*i)['items']
        for a in playlist1:
            list1.append(a['track']['id'])


    for i in list1:
        #print(i)
        if i in list2:
            count+=1
        
    return "The two playlists have "+str(round((count/(length1+length2-count))*100, 2))+"%"+' in common'
    
print(comparePlaylists(id1, id2))