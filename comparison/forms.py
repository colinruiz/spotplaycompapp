from django import forms
from .models import Dropdown
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .credentials import CLIENT_ID, CLIENT_SECRET

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
    CHOICES = [(playlist['id'], playlist['name']) for playlist in playlists] + [('other', 'Other')]

    choice_field = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'showInput(this)'}), label='Select Playlist:')
    text_field = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'display:none;'}), label='')







