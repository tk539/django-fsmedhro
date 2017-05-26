from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    StringRelatedField,
)
from exoral.models import Pruefer, Frage, Testat, Kommentar, Protokoll


"""
Frage-Serializers
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
            'score',
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
            'id',
            'datum',
            'text',
            'antwort',
            'testat',
            'pruefer',
            'score',
            #'created_by',
            'created_date',
            #'modified_by',
            'modified_date',
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


"""
Kommentar-Serializers
"""


class KommentarUpdateSerializer(ModelSerializer):

    class Meta:
        model = Kommentar
        fields = [
            #'id',
            'text',
            'pruefer',
            #'created_by',
            #'created_date',
            #'modified_by',
            #'modified_date',
            #'version',
        ]


class KommentarListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='exoral-api:kommentar_detail',
    )
    class Meta:
        model = Kommentar
        fields = [
            'url',
            'id',
            'text',
            'pruefer',
            #'created_by',
            'created_date',
            #'modified_by',
            'modified_date',
            #'version',
        ]


class KommentarDetailSerializer(ModelSerializer):
    pruefer = SerializerMethodField()
    created_by = SerializerMethodField()
    modified_by = SerializerMethodField()

    class Meta:
        model = Kommentar
        fields = [
            'id',
            'text',
            'pruefer',
            'created_by',
            'created_date',
            'modified_by',
            'modified_date',
            'version',
        ]

    def get_pruefer(self, obj):
        return obj.pruefer.get_full_name()

    def get_created_by(self, obj):
        return obj.created_by.username

    def get_modified_by(self, obj):
        return obj.modified_by.username


"""
Protokoll-Serializers
"""


class ProtokollUpdateSerializer(ModelSerializer):

    class Meta:
        model = Protokoll
        fields = [
            #'id',
            'datum',
            'text',
            'pruefer',
            'testat',
            #'created_by',
            #'created_date',
            #'modified_by',
            #'modified_date',
            #'version',
        ]


class ProtokollListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='exoral-api:protokoll_detail',
    )
    class Meta:
        model = Protokoll
        fields = [
            'url',
            'id',
            'datum',
            'text',
            'pruefer',
            'testat',
            #'created_by',
            'created_date',
            #'modified_by',
            'modified_date',
            #'version',
        ]


class ProtokollDetailSerializer(ModelSerializer):
    pruefer = SerializerMethodField()
    testat = SerializerMethodField()
    created_by = SerializerMethodField()
    modified_by = SerializerMethodField()

    class Meta:
        model = Protokoll
        fields = [
            'id',
            'datum',
            'text',
            'pruefer',
            'testat',
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


"""
Testat-Serializer
"""


class TestatListSerializer(ModelSerializer):
    #url = HyperlinkedIdentityField(
    #    view_name='exoral-api:testat_detail',
    #)
    #studiengang = StringRelatedField(many=True) #SerializerMethodField()
    #studienabschnitt = StringRelatedField(many=True) #SerializerMethodField()
    #fach_bezeichnung = StringRelatedField(many=True) #SerializerMethodField()
    class Meta:
        model = Testat
        fields = [
            #'url',
            'id',
            'bezeichnung',
            'studiengang',
            'studienabschnitt',
            'fach',
            'active',
        ]


"""
Prüfer-Serializers
"""


class PrueferListSerializer(ModelSerializer):
    fach_bezeichnung = SerializerMethodField()
    full_name = SerializerMethodField()
    class Meta:
        model = Pruefer
        fields = [
            'id',
            'titel',
            'vorname',
            'nachname',
            'full_name',
            'active',
            'fach',
            'fach_bezeichnung'
        ]

    def get_fach_bezeichnung(self, obj):
        if obj.fach:
            return obj.fach.bezeichnung
        else:
            return None

    def get_full_name(self, obj):
        return obj.get_full_name()