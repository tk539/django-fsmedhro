from rest_framework.serializers import ModelSerializer
from fsmedhrocore.models import Studienabschnitt, Studiengang, Gender, FachschaftUser, Dozent, Fach


class StudienabschnittSerializer(ModelSerializer):
    class Meta:
        model = Studienabschnitt
        fields = '__all__' # TODO: specify for deployment !


"""
Fach-Serializer
"""


class FachListSerializer(ModelSerializer):
    class Meta:
        model = Fach
        fields = [
            #'url',
            'id',
            'bezeichnung',
        ]
