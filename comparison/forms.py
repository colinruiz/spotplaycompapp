from django import forms
from .models import Dropdown

class DropdownForm(forms.Form):
    CHOICES = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('other', 'Other')
    ]
    choice_field = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'showInput(this)'}), label='Select Playlist:')
    text_field = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'display:none;'}), label='')







