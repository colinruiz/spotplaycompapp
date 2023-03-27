from django.shortcuts import render
import requests
import base64
import spotipy
# Create your views here.
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth, CacheHandler
from .forms import DropdownForm
import os
import spotipy


CLIENT_ID = "0eb27e7c8598493fba46f54e10550e4f"
CLIENT_SECRET = "c520c87edc224b069f8ef996a5287642"
REDIRECT_URI = "http://127.0.0.1:8000/spotify/redirect"
SCOPES= "user-read-playback-state app-remote-control streaming user-library-read playlist-read-private playlist-read-collaborative"


def home(request):
    return render(request, 'home.html')

def spotify_login(request):

    #client_id = CLIENT_ID
    #redirect_uri = REDIRECT_URI
    #scope = SCOPES
    #auth_url = f'https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}'
    #return redirect(auth_url)



    auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                scope=SCOPES, show_dialog=True)

    # If there is no authorization code, redirect the user to the Spotify login page
    # if not request.GET.get('code'):
    #     auth_url = auth_manager.get_authorize_url()
    #     return redirect(auth_url)

    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)
    # If there is an authorization code, exchange it for an access token and refresh token
    # auth_manager.get_access_token(request.GET.get('code'))
    # return render(request, 'success.html')


def spotify_callback(request):

    
    #client_id = CLIENT_ID
    #client_secret = CLIENT_SECRET
    #redirect_uri = REDIRECT_URI
    #code = request.GET.get('code')
    #auth_header = f'{client_id}:{client_secret}'
    #b64_auth_header = base64.b64encode(auth_header.encode('ascii')).decode('ascii')
    #headers = {'Authorization': f'Basic {b64_auth_header}'}
    #data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': redirect_uri}
    #response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    #token = response.json()['access_token']
    #return redirect('/playlists')


#def playlists(request):
    #auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=SCOPES)
    #sp = spotipy.Spotify(auth_manager=auth_manager)
    #playlists = sp.current_user_playlists()
    #CHOICES = [(playlist['id'], playlist['name']) for playlist in playlists] + [('other', 'Other')]
    #dropdown_form1 = DropdownForm(choices=CHOICES)
    #dropdown_form2 = DropdownForm(choices=CHOICES)
    #return render(request, 'success.html', context = {'dropdown_form1': dropdown_form1, 'dropdown_form2': dropdown_form2})




    auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                scope=SCOPES)

    # Check if the authorization code is in the request
    if request.GET.get('code'):
        try:
            # Get the authorization code from the request
            code = request.GET['code']
            # Exchange the authorization code for an access token and a refresh token
            token_info = auth_manager.get_access_token(code)
            # Save the access token and refresh token to the cache
            auth_manager.cache_handler.save_token_to_cache(token_info)

            if request.method == 'POST':
                dropdown_form1 = DropdownForm(request.POST)
                if dropdown_form1.is_valid():
                    dropdown_choice = dropdown_form1.cleaned_data['choice_field']
                    user_input = dropdown_form1.cleaned_data['text_field']
            # Do something with the form data
            else:
                dropdown_form1 = DropdownForm()

            if request.method == 'POST':
                dropdown_form2 = DropdownForm(request.POST)
                if dropdown_form2.is_valid():
                    dropdown_choice = dropdown_form2.cleaned_data['choice_field']
                    user_input = dropdown_form2.cleaned_data['text_field']
            # Do something with the form data
            else:
                dropdown_form2 = DropdownForm()
            # Redirect the user to the success page
            return render(request, 'success.html', context = {'dropdown_form1': dropdown_form1, 'dropdown_form2': dropdown_form2})
        except Exception as e:
            # Something went wrong during the token exchange
            print(f"Token exchange error: {e}")
            return render(request, 'failure.html')
    else:
        # Check if the access token is still valid
        token_info = auth_manager.cache_handler.get_cached_token()
        if auth_manager.validate_token(token_info):
            # Access token is still valid, refresh it
            token_info = auth_manager.refresh_access_token(token_info['refresh_token'])
            # Save the new access token to the cache
            auth_manager.cache_handler.save_token_to_cache(token_info)

            if request.method == 'POST':
                dropdown_form1 = DropdownForm(request.POST)
                if dropdown_form1.is_valid():
                    dropdown_choice = dropdown_form1.cleaned_data['choice_field']
                    user_input = dropdown_form1.cleaned_data['text_field']
            # Do something with the form data
            else:
                dropdown_form1 = DropdownForm()

            if request.method == 'POST':
                dropdown_form2 = DropdownForm(request.POST)
                if dropdown_form2.is_valid():
                    dropdown_choice = dropdown_form2.cleaned_data['choice_field']
                    user_input = dropdown_form2.cleaned_data['text_field']
            # Do something with the form data
            else:
                dropdown_form2 = DropdownForm()
            # Redirect the user to the success page
            return render(request, 'success.html', context = {'dropdown_form1': dropdown_form1, 'dropdown_form2': dropdown_form2})

        else:
            # Access token is not valid, redirect the user to the Spotify login page
            auth_url = auth_manager.get_authorize_url()
            return redirect(auth_url)
        

def logout_view(request):
    access_token = request.session.get('access_token')
    if access_token:
        revoke_url = 'https://accounts.spotify.com/api/token/revoke'
        params = {'token': access_token}
        response = requests.delete(revoke_url, params=params)
        if response.status_code == 200:
            del request.session['access_token']
            # Perform any additional logout tasks
            return render(request, 'home.html')
    return render(request, 'home.html')

    
def dropdown_view1(request):
    print("View executed!")
    if request.method == 'POST':
        dropdown_form1 = DropdownForm(request.POST)
        if dropdown_form1.is_valid():
            dropdown_choice = dropdown_form1.cleaned_data['dropdown']
            # Do something with the form data
    else:
        dropdown_form1 = DropdownForm()
      # Add this line to ensure the view is executing
    print(dropdown_form1)
    
    return render(request, 'success.html', context = {'dropdown_form1': dropdown_form1})


def dropdown_view2(request):
    if request.method == 'POST':
        dropdown_form2 = DropdownForm(request.POST)
        if dropdown_form2.is_valid():
            dropdown_choice = dropdown_form2.cleaned_data['dropdown']
            user_input = dropdown_form2.cleaned_data['user_input']
            # Do something with the form data
    else:
        dropdown_form2 = DropdownForm()
    
    return render(request, 'success.html', context = {'dropdown_form2': dropdown_form2})




