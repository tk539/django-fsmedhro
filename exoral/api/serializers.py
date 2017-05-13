from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)
from exoral.models import Pruefer, Frage


"""
Prüfer-Serializers
"""
class PrueferCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Pruefer
        fields = [
            #'id',
            'titel',
            'vorname',
            'nachname',
            'fach',
            # 'active',
        ]


class PrueferDetailSerializer(ModelSerializer):
    class Meta:
        model = Pruefer
        fields = [
            'id',
            'titel',
            'vorname',
            'nachname',
            'fach',
            'active',
        ]


class PrueferListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='exoral-api:pruefer_detail',
    )
    fach = SerializerMethodField()
    full_name = SerializerMethodField()
    class Meta:
        model = Pruefer
        fields = [
            'url',
            'full_name',
            'fach',
            #'active',
        ]

    def get_fach(self, obj):
        if obj.fach:
            return obj.fach.bezeichnung
        else:
            return None

    def get_full_name(self, obj):
        return obj.get_full_name()


"""
Prüfer-Serializers
"""
class FrageUpdateSerializer(ModelSerializer):

    class Meta:
        model = Frage
        fields = [
            #'id',
            'datum',
            'text',
            'antwort',
            'testat',
            'pruefer',
            #'score',
            #'created_by',
            #'created_date',
            #'modified_by',
            #'modified_date',
            #'version',
        ]


class FrageListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='exoral-api:frage_detail',
    )
    class Meta:
        model = Frage
        fields = [
            'url',
            'datum',
            'text',
            'antwort',
            'testat',
            'pruefer',
            #'id',
            #'score',
            #'created_by',
            #'created_date',
            #'modified_by',
            #'modified_date',
            #'version',
        ]


class FrageDetailSerializer(ModelSerializer):
    testat = SerializerMethodField()
    pruefer = SerializerMethodField()
    created_by = SerializerMethodField()
    modified_by = SerializerMethodField()

    class Meta:
        model = Frage
        fields = [
            'id',
            'datum',
            'text',
            'antwort',
            'testat',
            'pruefer',
            'score',
            'created_by',
            'created_date',
            'modified_by',
            'modified_date',
            'version',
        ]

    def get_testat(self, obj):
        return obj.testat.bezeichnung

    def get_pruefer(self, obj):
        return obj.pruefer.get_full_name()

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_modified_by(self, obj):
        return obj.modified_by.username