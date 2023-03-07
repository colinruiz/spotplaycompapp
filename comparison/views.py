from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth
CLIENT_ID = "0eb27e7c8598493fba46f54e10550e4f"
CLIENT_SECRET = "c520c87edc224b069f8ef996a5287642"
REDIRECT_URI = "http://127.0.0.1:8000/spotify/redirect"

def home(request):
    return render(request, 'home.html')

def spotify_login(request):
    auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                scope='user-library-read')

    # If there is no authorization code, redirect the user to the Spotify login page
    if not request.GET.get('code'):
        auth_url = auth_manager.get_authorize_url()
        return redirect(auth_url)

    # If there is an authorization code, exchange it for an access token and refresh token
    auth_manager.get_access_token(request.GET.get('code'))
    return render(request, 'success.html')


def spotify_callback(request):
    auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                scope='user-library-read')
    if request.GET.get('code'):
        auth_manager.get_access_token(request.GET.get('code'))
        return render(request, 'success.html')
    else:
        return render(request, 'failure.html')