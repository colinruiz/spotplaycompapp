from django.shortcuts import render
import requests
# Create your views here.
from django.shortcuts import redirect
from spotipy.oauth2 import SpotifyOAuth, CacheHandler
from .forms import MyDataForm, SecondForm
from django.http import HttpResponse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth




CLIENT_ID = "0eb27e7c8598493fba46f54e10550e4f"
CLIENT_SECRET = "c520c87edc224b069f8ef996a5287642"
REDIRECT_URI = "http://127.0.0.1:8000/spotify/redirect"
SCOPES= "user-read-playback-state app-remote-control streaming user-library-read"

auth_manager = SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                                redirect_uri=REDIRECT_URI,
                                scope=SCOPES)
#from spotipy.cache_handler import SpotifyCacheHandler

#cache_handler = SpotifyCacheHandler(cache_path=".cache")

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


def spotify_callback(request):
    

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
        
        

def form(request):
    if request.method == 'POST':
        playlist_id1 = request.POST.get('playlist_id1')
        # playlist_id2 = request.POST.get('playlist_id2')
        with open('playlist_id1.txt', 'w') as f:
            f.write(playlist_id1)
        # if (playlist_id2=="" or playlist_id1==""):
        #     return HttpResponse('fail')
        # print(playlist_id1, playlist_id2)
        # Do something with the user_text
        #return HttpResponse('Success')
        print(playlist_id1)
    return render(request, 'success.html')

def formtwo(request):
    if request.method == 'POST':
        playlist_id2 = request.POST.get('playlist_id2')
        # playlist_id2 = request.POST.get('playlist_id2')
        with open('playlist_id2.txt', 'w') as f:
            f.write(playlist_id2)
        # if (playlist_id2=="" or playlist_id1==""):
        #     return HttpResponse('fail')
        # print(playlist_id1, playlist_id2)
        # Do something with the user_text
        #return HttpResponse('Success')
        
        # Do something with the user_text
        print(playlist_id2)
    return render(request, 'success.html')



def logout_view(request):
    # with open("playlist_id1.txt") as f:
    #     id1 = f.read()
    # with open("playlist_id2.txt") as f:
    #     id2 = f.read()
    # print(comparePlaylists(id1, id2))
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


def compare_playlists(request):
    with open('playlist_id1.txt', 'r') as f:
        playlist1_id = f.read()
    with open('playlist_id2.txt', 'r') as f:
        playlist2_id = f.read()
    
    # scopes for auth_manager
    scope = "user-read-playback-state app-remote-control streaming user-library-read"

    #sp = spotipy.Spotify(auth_manager)
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
        playlist2=sp.playlist_tracks(playlist2_id, limit=100, offset=100*k)['items']
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
        
    similarity = "The two playlists have " +str(round((count/(length1+length2-count))*100, 2))+"%"+' in common'
    return render(request, 'success.html', {'similarity': similarity})

# def calculate_playlists(request):
#     response = compare_playlists(request)
#     similarity = response.content.decode('utf-8')
#     return render(request, 'success.html', {'similarity': similarity})


    # if request.method == 'POST':
    #     form = MyDataForm(request.POST)
    #     print(request.POST) # print the submitted form data
    #     if form.is_valid():
    #         playlist_id = form.cleaned_data['playlist_id']
    #         print(playlist_id)
    #         form.save()
    #         context = {'form': form, 'success': True, 'playlist_id': playlist_id}
    #         return render(request, 'success.html', context)
    #     else:
    #         print("errors")
    #         print(form.errors) # print any validation errors
    # else:
    #     form = MyDataForm()
    # context = {'form': form, 'success': True}
    #return render(request, 'success.html', context)


# def formtwo(request):
#     if request.method == 'POST':
#         form = SecondForm(request.POST)
#         if form.is_valid():
#             playlist_id = form.cleaned_data['playlist_id']
#             # with open('playlist_ids_2.txt', 'a') as f:
#             #     f.write(playlist_id + '\n')
#             form.save()
#             context = {'form': form, 'success': True, 'playlist_id': playlist_id}
#             return render(request, 'success.html', context)
#     else:
#         form = SecondForm()
#     context = {'form': form}
#     return render(request, 'success.html', context)