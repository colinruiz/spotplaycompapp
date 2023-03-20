from django import forms
from .models import MyData, Second

class MyDataForm(forms.ModelForm):
    #playlist_id = forms.CharField(max_length=100)
    playlist_id = forms.CharField(label = "Playlist ID")
    
    class Meta:
        model = MyData
        fields = ['playlist_id']
        
class SecondForm(forms.ModelForm):
    #playlist_id = forms.CharField(max_length=100)
    playlist_id = forms.CharField(label = "Playlist ID")
    
    class Meta:
        model = Second
        fields = ['playlist_id']