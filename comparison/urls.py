from django.urls import path
from comparison.views import *

urlpatterns = [
    path('', home, name='home'),
    path('spotify/login/', spotify_login, name='spotify_login'),
    path('spotify/redirect/', spotify_callback, name='spotify_callback'),
    path('form/', form, name = 'form'),
    path('formtwo/', formtwo, name = 'formtwo'),
    path('logout/', logout_view, name='logout_view'),
    path('compare/playlists/',  compare_playlists, name = 'compare_playlists')
    path('success/', success, name='success')
]