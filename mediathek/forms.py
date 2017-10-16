from mediathek.models import Sammelbestellung
from django import forms

class SammelbestForm(forms.ModelForm):
    class Meta:
        model = Sammelbestellung
        fields = ['bezeichnung', 'start', 'ende', 'abgeschlossen']
        widgets = {
            'start': forms.TextInput(attrs={'placeholder': 'JJJJ-MM-TT ss:mm'}),
            'ende': forms.TextInput(attrs={'placeholder': 'JJJJ-MM-TT ss:mm'}),
        }