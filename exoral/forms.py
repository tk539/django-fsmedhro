from exoral.models import Frage, Kommentar, Protokoll
from django.forms import ModelForm


class FrageForm(ModelForm):
    class Meta:
        model = Frage
        fields = ['datum', 'text', 'antwort', 'pruefer', 'testat']

class ProtokollForm(ModelForm):
    class Meta:
        model = Protokoll
        fields = ['datum', 'text', 'pruefer', 'testat']

class KommentarForm(ModelForm):
    class Meta:
        model = Kommentar
        fields = ['text', 'pruefer']