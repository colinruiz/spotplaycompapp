from django import forms
from .models import Dropdown
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from .credentials import CLIENT_ID, CLIENT_SECRET


class DropdownForm(forms.Form):
    CHOICES = [('other', 'Other')]

    choice_field = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'showInput(this)'}), label='Select Playlist:')
    text_field = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'display:none;'}), label='')







