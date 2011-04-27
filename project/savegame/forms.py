from django.forms import ModelForm
from savegame.models import *
from django.contrib.auth.models import User
from django import forms

class RegForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    repassword = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean_username(self):
        entry = self.cleaned_data['username']
        try:
            User.objects.get(username=entry) #using get because username should be unique
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError("That username already exists!")
        return entry

    def clean_repassword(self):
        entry = self.cleaned_data['password']
        reentry = self.cleaned_data['repassword']
        if entry != reentry:
            raise forms.ValidationError("The passwords do not match!")
        return reentry


class UploadGameForm(ModelForm):
    class Meta:
        model = UploadedGame
        exclude = ('user', 'datetime', 'upvote', 'downvote')