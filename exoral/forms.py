from exoral.models import Frage
from django.forms import ModelForm


class FrageForm(ModelForm):
    class Meta:
        model = Frage
        fields = ['datum', 'text', 'antwort', 'pruefer', 'testat']