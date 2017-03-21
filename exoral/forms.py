from exoral.models import Frage
from exoral.models import Kommentar
from django.forms import ModelForm


class FrageForm(ModelForm):
    class Meta:
        model = Frage
        fields = ['datum', 'text', 'antwort', 'pruefer', 'testat']

class KommentarForm(ModelForm):
    class Meta:
        model = Kommentar
        fields = ['text', 'pruefer']