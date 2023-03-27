from django import forms
from .models import Dropdown
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from spotipy.oauth2 import SpotifyOAuth
import os
#from .views import getUserPlaylist


#SCOPES= "user-read-playback-state app-remote-control streaming user-library-read playlist-read-private playlist-read-collaborative"




# client_credentials_manager = SpotifyClientCredentials(
#     client_id=CLIENT_ID,
#     client_secret=CLIENT_SECRET
# )
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# playlists = []
# results = sp.current_user_playlists()
# while results:
#     playlists.extend(results['items'])
#     if results['next']:
#         results = sp.next(results)
#     else:
#         break

# def getUserPlaylist():
#     try:
#         os.remove(".cache")
#     except:
#         ()

#     # scopes for auth_manager
#     scope = "user-read-playback-state app-remote-control streaming user-library-read"

#     sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, scope=scope, redirect_uri=REDIRECT_URI))
    
#     # Get playlists of the current user
#     user_id = sp.current_user()['id']
#     print(f"Current User ID: {user_id}")
#     total = sp.current_user_playlists()['total']
#     playlists = []
#     for i in range((total//50)+1):
#         playlists += sp.current_user_playlists(limit=50, offset=50*i)["items"]
    
#     # Get playlists of a specified user
#     other_user_id = ''
#     print(f"Other User ID: {other_user_id}")
#     total = sp.user_playlists(other_user_id)['total']
#     other_playlists = []
#     for i in range((total//50)+1):
#         other_playlists += sp.user_playlists(other_user_id, limit=50, offset=50*i)["items"]
    
#     # Combine and format the playlists
#     all_playlists = playlists + other_playlists
#     id_name = [{'id': playlist["id"], 'name': playlist["name"]} for playlist in all_playlists]
#     return id_name, all_playlists


#def getUserPlaylist():
    #try:
    #    os.remove(".cache")
    #except:
    #    ()

    # scopes for auth_manager
    #scope = "user-read-playback-state app-remote-control streaming user-library-read"

    #sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, scope=scope, redirect_uri=REDIRECT_URI))
    #sp = spotipy.Spotify(auth_manager=SpotifyOAuth('f8a3f82ba99d46a694d89bc1cdc1cb09', '0dcbdb4f9fd0496683a16c01c93a9377', scope=scope, redirect_uri="http://127.0.0.1:8000/spotify/redirect"))
    
    #extract the user
    #user = sp.current_user()
    #user_id = user['id']
    #print(user_id)
    # total = sp.current_user_playlists()['total']
    # print(total)
    #playlists = []
    #results = sp.user_playlists(user_id)
    #while results:
    #    playlists.extend(results['items'])
    #    if results['next']:
    #        results = sp.next(results)
    #    else:
    #        break
    # playlists = []
    # for i in range((total//50)+1):
    #     playlists += sp.current_user_playlists(limit=50, offset=50*i)["items"]
    
    #id_name = []
    #for playlist in playlists:
    #    id_name.append({'id': playlist["id"], 'name': playlist["name"]})
    #    print(playlist["name"])
    #return id_name, playlists


client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


playlists = []
results = sp.current_user_playlists()
while results:
    playlists.extend(results['items'])
    if results['next']:
        results = sp.next(results)
    else:
        break


class DropdownForm(forms.Form):
    CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('other', 'Other')
    ]
    choice_field = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'showInput(this)'}), label='Select Playlist:')
    text_field = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'display:none;'}), label='')







