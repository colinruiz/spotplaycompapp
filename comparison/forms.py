from django import forms
from .models import MyData, Second, Dropdown, Dropdown2

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


class DropdownForm(forms.Form):
    dropdown_choices = [('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3')]
    dropdown = forms.ChoiceField(choices=dropdown_choices)
    user_input = forms.CharField(label = "Playlist Link")

    class Meta:
        model = Dropdown
        fields = ['dropdown', 'user_input']


class DropdownForm2(forms.Form):
    dropdown_choices = [('option1', 'Option 1'), ('option2', 'Option 2'), ('option3', 'Option 3')]
    dropdown = forms.ChoiceField(choices=dropdown_choices)
    user_input = forms.CharField(label = "Playlist Link")

    class Meta:
        model = Dropdown2
        fields = ['dropdown', 'user_input']