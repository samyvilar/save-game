from django.forms import ModelForm
from savegame.models import *


class UploadGameForm(ModelForm):
    class Meta:
        model = UploadedGame
        exclude = ('user', 'datetime', 'upvote', 'downvote')