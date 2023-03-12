from django import forms
from .models import Post
from django.forms import ModelForm

class Postform(ModelForm):
    class Meta:       
        model = Post
        fields = ['textarea']
        widgets = {
            'textarea': forms.Textarea(attrs={'class': 'postarea', "placeholder": 'New post', "rows": '2'}),
        }
        labels = {
            'textarea': '',
        }