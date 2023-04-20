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
from .credentials import *




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
    token_info = auth_manager.get_access_token(code, check_cache=False)

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

    CHOICES = [('', 'Select Playlist...')]
    CHOICES.extend([(playlist['id'], playlist['name']) for playlist in playlists] + [('other', 'Other')])
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
    #playlists = playlists_response.json()['items']

    dropdown_form1 = DropdownForm(choices=request.session.get('choices', []))
    dropdown_form2 = DropdownForm(choices=request.session.get('choices', []))

    if request.method == 'POST':
        print('View executed')

        value_from_formone = request.POST.get('data1')
        value_from_formtwo = request.POST.get('data2')

        print(value_from_formone)
        print(value_from_formtwo)

        
        #sp = spotipy.Spotify(auth_manager)
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, scope=SCOPES, redirect_uri=REDIRECT_URI))
        #sp = spotipy.Spotify(auth_manager=SpotifyOAuth('f8a3f82ba99d46a694d89bc1cdc1cb09', '0dcbdb4f9fd0496683a16c01c93a9377', scope=scope, redirect_uri="http://127.0.0.1:8000/spotify/redirect"))

        

        # Get the tracks from both playlists
        valid1=None
        valid2=None
        playlist1_img=None
        playlist2_img=None
        try:
            playlist1 = sp.playlist(value_from_formone)
            valid1=True
            playlist1_img = playlist1['images'][0]['url']
        except:
            valid1=False

        try:
            playlist2 = sp.playlist(value_from_formtwo)
            valid2=True
            playlist2_img = playlist2['images'][0]['url']
        except:
            valid2=False

        #playlist1_img = playlist1['images'][0]['url']
        #playlist2_img = playlist2['images'][0]['url']
        if(valid1 and valid2):
            length1=sp.playlist(value_from_formone)['tracks']['total']
            length2=sp.playlist(value_from_formtwo)['tracks']['total']
            #tracks1 = set([track['track']['id'] for track in playlist1['tracks']['items'] if track['track'] is not None])
            #tracks2 = set([track['track']['id'] for track in playlist2['tracks']['items'] if track['track'] is not None])
            
            tracks1 = []
            for k in range((length2//100)+1):
                playlist2=sp.playlist_tracks(value_from_formtwo, limit=100, offset=100*(k))['items']
                for a in playlist2:
                    tracks1.append(a['track'])
                        
            tracks2 = []
            for i in range((length1//100)+1):
                playlist1=sp.playlist_tracks(value_from_formone, limit=100, offset=100*i)['items']
                for a in playlist1:
                    tracks2.append(a['track'])
            
            # counts the number of shared tracks
            count=0
                    
            shared_tracks = []        
            for i in tracks1:
                #print(i)
                for j in tracks2:
                    if i['id'] == j['id']:
                        count+=1
                        str1=(i['name']+" - "+ i['artists'][0]['name'])
                        shared_tracks.append(str1)
                        tracks2.remove(j)
            #tracks1=set(tracks1)
            #tracks2=set(tracks2)
            # Calculate the percentage of similar songs
            #num_similar = len(tracks1.intersection(tracks2))
            #num_total = len(tracks1.union(tracks2))
            percentage_similarity = round((count / (length1+length2-count)) * 100, 2)
            

            
            #print(playlist1.keys())
            #for track in playlist1:
            #    if track['id'] is not None and track['id'] in tracks2:
            #        shared_tracks.append(track['name'])
            response = {
            'percentage_similarity': percentage_similarity,
            'playlist1': playlist1,
            'playlist2': playlist2,
            'shared_tracks': shared_tracks,
            'count' : count,
            'playlist1_img': playlist1_img,
            'playlist2_img': playlist2_img,
            'validPlaylist': (valid1 and valid2)
        }
        else: 
            response={
            'playlist1_img': playlist1_img,
            'playlist2_img': playlist2_img,
            'validPlaylist': (valid1 and valid2)
            }
        #print(percentage_similarity)
        
        #print(valid1, valid2, valid1 and valid2)
        

        return JsonResponse(response)
        
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
        

    



