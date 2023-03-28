from django.shortcuts import render
import requests
import base64
import spotipy
import spotipy.util as util
# Create your views here.
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth, CacheHandler
from .forms import DropdownForm
import os
from django.views.decorators.cache import never_cache


CLIENT_ID = "0eb27e7c8598493fba46f54e10550e4f"
CLIENT_SECRET = "c520c87edc224b069f8ef996a5287642"
REDIRECT_URI = "http://127.0.0.1:8000/spotify/redirect"
SCOPES= "user-read-playback-state app-remote-control streaming user-library-read playlist-read-private playlist-read-collaborative"


def home(request):
    return render(request, 'home.html')

def spotify_login(request):

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

@never_cache
def spotify_callback(request):
    
    auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                scope=SCOPES)

    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    redirect_uri = REDIRECT_URI
    
    # Exchange the authentication code for an access token and refresh token
    code = request.GET.get('code')
    #sp_oauth = spotipy.oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=SCOPES)
    token_info = auth_manager.get_access_token(code)

    # Check if the authorization code is in the request
    if not token_info['access_token']:
        try:
            code = request.GET['code']
            # Exchange the authorization code for an access token and a refresh token
            token_info = auth_manager.get_access_token(code)

        except Exception as e:
            # Something went wrong during the token exchange
            print(f"Token exchange error: {e}")
            return render(request, 'failure.html')
    
    # Save the access token and refresh token in the session
    request.session['access_token'] = token_info['access_token']
    request.session['refresh_token'] = token_info['refresh_token']

    # Use spotipy to get the user's playlists
    access_token = token_info['access_token']
    sp = spotipy.Spotify(auth=access_token)
    playlists = []
    results = sp.current_user_playlists()
    while results:
        playlists.extend(results['items'])
        if results['next']:
            results = sp.next(results)
        else:
            break

    CHOICES = [(playlist['id'], playlist['name']) for playlist in playlists] + [('other', 'Other')]
    request.session['choices'] = CHOICES

    return redirect('success')



@never_cache
def success(request):
    # Set up the authentication credentials

    print(request.session['access_token'])
    print(request.session['refresh_token'])
    print(request.session['choices'])


    access_token = request.session.get('access_token')
    sp = spotipy.Spotify(auth=access_token)
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    playlists_response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)
    playlists = playlists_response.json()['items']

    dropdown_form1 = DropdownForm(choices=request.session.get('choices', []))
    dropdown_form2 = DropdownForm(choices=request.session.get('choices', []))

    
    # Render the success template with the playlist names
    return render(request, 'success.html', context = {'dropdown_form1': dropdown_form1, 'dropdown_form2': dropdown_form2})
        

def logout_view(request):
    access_token = request.session.get('access_token')
    if access_token:
        revoke_url = 'https://accounts.spotify.com/api/token/revoke'
        params = {'token': access_token}
        response = requests.delete(revoke_url, params=params)
        if response.status_code == 200:
            del request.session['access_token']
            del request.session['refresh_token']
            del request.session['choices']
            # Perform any additional logout tasks
            return render(request, 'home.html')

    del request.session['access_token']
    del request.session['refresh_token']
    del request.session['choices']

    return render(request, 'home.html')

#BQBUC0u69Ae4W02sjOWSgGnzJC09hUDc32Z-7yQKauHfeA7YgmT3sg6uySe2P8jcsW6dMewgMvggcsFY4QjXgyv1oUrM9vmG7QGpP263tHjH0-i8P2RvcdeOO_MfmHX9BRVzKoHFR3YC5NwwB-hYcLgThGfbi2WcQwBr38dWufTRXSscsokeu7oS38n5UmTPjt0jP6RQlNkm3rsz9kunzuY4FlkfHIffFgg-L9N8plcxIg
#AQCvTlniNN9o-OTmwmS5BnD2J3edhgAdndaJjsDvat9AV6IdVrogKEnuXrneNLZgCuo5-Zs9LHj-WQO2IS56gq6bd665pzLqqArMN_ce_scyoPSMdEya_OTYmmq3A_GGDhA


    
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




