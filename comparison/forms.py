from django import forms
from .models import MyData

class MyDataForm(forms.ModelForm):
    #playlist_id = forms.CharField(max_length=100)
    playlist_id = forms.CharField(label = "Playlist ID")
    
    class Meta:
        model = MyData
        fields = ['playlist_id']