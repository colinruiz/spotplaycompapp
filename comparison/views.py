from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth
CLIENT_ID = "0eb27e7c8598493fba46f54e10550e4f"
CLIENT_SECRET = "c520c87edc224b069f8ef996a5287642"
REDIRECT_URI = "http://127.0.0.1:8000/spotify/redirect"
SCOPES= "user-library-read"
#from spotipy.cache_handler import SpotifyCacheHandler

#cache_handler = SpotifyCacheHandler(cache_path=".cache")

def home(request):
    return render(request, 'home.html')

def spotify_login(request):
    auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                scope=SCOPES)

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
            # Redirect the user to the success page
            return render(request, 'success.html')
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
            # Redirect the user to the success page
            return render(request, 'success.html')
        else:
            # Access token is not valid, redirect the user to the Spotify login page
            auth_url = auth_manager.get_authorize_url()
            return redirect(auth_url)