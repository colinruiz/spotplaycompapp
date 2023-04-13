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
from django.http import JsonResponse


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
    access_token = request.session.get('access_token')
    sp = spotipy.Spotify(auth=access_token)
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    playlists_response = requests.get('https://api.spotify.com/v1/me/playlists', headers=headers)
    playlists = playlists_response.json()['items']

    dropdown_form1 = DropdownForm(choices=request.session.get('choices', []))
    dropdown_form2 = DropdownForm(choices=request.session.get('choices', []))

    if request.method == 'POST':
        print('View executed')
        form1_data = request.POST.get('data1')
        form2_data = request.POST.get('data2')

        print(form1_data)
        print(form2_data)


        #sp = spotipy.Spotify(auth_manager)
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, scope=SCOPES, redirect_uri=REDIRECT_URI))
        #sp = spotipy.Spotify(auth_manager=SpotifyOAuth('f8a3f82ba99d46a694d89bc1cdc1cb09', '0dcbdb4f9fd0496683a16c01c93a9377', scope=scope, redirect_uri="http://127.0.0.1:8000/spotify/redirect"))

        # counts the number of shared tracks
        count=0

        # Get the tracks from both playlists
        playlist1 = sp.playlist(form1_data)
        playlist2 = sp.playlist(form2_data)
        
        tracks1 = set([track['track']['id'] for track in playlist1['tracks']['items'] if track['track'] is not None])
        tracks2 = set([track['track']['id'] for track in playlist2['tracks']['items'] if track['track'] is not None])
        
        # Calculate the percentage of similar songs
        num_similar = len(tracks1.intersection(tracks2))
        num_total = len(tracks1.union(tracks2))
        percentage_similarity = round(num_similar / num_total * 100, 2)

        return render(request, 'success.html', context = {'dropdown_form1': dropdown_form1, 'dropdown_form2': dropdown_form2, 'percent_similarity': percentage_similarity})

    else:
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

def compare_playlists(request):
    print("View Executed")
    if request.method == 'POST':
        
        form1_data = request.POST.get('form1_data')
        form2_data = request.POST.get('form2_data')

        print('Made it!')
        print(request.method)  # should be POST
        print(request.POST)  # should contain the form data
        print(request.POST.get('data1'))


        #sp = spotipy.Spotify(auth_manager)
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, scope=SCOPES, redirect_uri=REDIRECT_URI))
        #sp = spotipy.Spotify(auth_manager=SpotifyOAuth('f8a3f82ba99d46a694d89bc1cdc1cb09', '0dcbdb4f9fd0496683a16c01c93a9377', scope=scope, redirect_uri="http://127.0.0.1:8000/spotify/redirect"))

        # counts the number of shared tracks
        count=0

        # Get the tracks from both playlists
        playlist1 = sp.playlist(form1_data)
        playlist2 = sp.playlist(form2_data)
        
        tracks1 = set([track['track']['id'] for track in playlist1['tracks']['items'] if track['track'] is not None])
        tracks2 = set([track['track']['id'] for track in playlist2['tracks']['items'] if track['track'] is not None])
        
        # Calculate the percentage of similar songs
        num_similar = len(tracks1.intersection(tracks2))
        num_total = len(tracks1.union(tracks2))
        percentage_similar = round(num_similar / num_total * 100, 2)

        response_data = {
            'message': 'Playlists are ' + percentage_similar + ' similar',
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method.'})
        

    



