from fsmedhrocore.models import FachschaftUser
from django.forms import ModelForm
from django.contrib.auth.models import User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class FachschaftUserForm(ModelForm):
    class Meta:
        model = FachschaftUser
        fields = ['gender', 'nickname', 'studiengang', 'studienabschnitt']