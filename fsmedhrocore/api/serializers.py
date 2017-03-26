from rest_framework.serializers import ModelSerializer
from fsmedhrocore.models import Studienabschnitt, Studiengang, Gender, FachschaftUser, Dozent


class StudienabschnittSerializer(ModelSerializer):
    class Meta:
        model = Studienabschnitt
        fields = '__all__' # TODO: specify for deployment !
