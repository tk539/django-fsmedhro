from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.generics import (
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
)

from exoral.models import (
    Pruefer,
    Frage,
    Testat,
    Kommentar,
)

from .serializers import (
    PrueferListSerializer,
    FrageListSerializer,
    FrageDetailSerializer,
    FrageUpdateSerializer,
    TestatListSerializer,
    KommentarListSerializer,
    KommentarDetailSerializer,
    KommentarUpdateSerializer,
)


"""
Prüfer-API-Views
"""


class PrueferListAPIView(ListCreateAPIView):
    queryset = Pruefer.objects.all()
    serializer_class = PrueferListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['titel', 'nachname', 'vorname', 'fach__bezeichnung']

    # support for multiple objects creation
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(PrueferListAPIView, self).get_serializer(*args, **kwargs)


"""
Frage-API-Views
"""


class FrageListAPIViev(ListCreateAPIView):
    queryset = Frage.objects.all()
    serializer_class = FrageListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['text', 'antwort', 'pruefer__nachname', 'testat__bezeichnung', 'modified_by__username']

    def perform_create(self, serializer):
        serializer.save(modified_by=self.request.user)

    # support for multiple objects creation
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(FrageListAPIViev, self).get_serializer(*args, **kwargs)


class FrageDetailAPIViev(RetrieveAPIView):
    queryset = Frage.objects.all()
    serializer_class = FrageDetailSerializer


class FrageDeleteAPIViev(DestroyAPIView):
    queryset = Frage.objects.all()
    serializer_class = FrageDetailSerializer


class FrageUpdateAPIViev(RetrieveUpdateAPIView):
    queryset = Frage.objects.all()
    serializer_class = FrageUpdateSerializer

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


"""
Kommentar-API-Views
"""


class KommentarListAPIViev(ListCreateAPIView):
    queryset = Kommentar.objects.all()
    serializer_class = KommentarListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['text', 'pruefer__nachname', 'modified_by__username']

    def perform_create(self, serializer):
        serializer.save(modified_by=self.request.user)

    # support for multiple objects creation
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(KommentarListAPIViev, self).get_serializer(*args, **kwargs)


class KommentarDetailAPIViev(RetrieveAPIView):
    queryset = Kommentar.objects.all()
    serializer_class = KommentarDetailSerializer


class KommentarDeleteAPIViev(DestroyAPIView):
    queryset = Kommentar.objects.all()
    serializer_class = KommentarDetailSerializer


class KommentarUpdateAPIViev(RetrieveUpdateAPIView):
    queryset = Kommentar.objects.all()
    serializer_class = KommentarUpdateSerializer

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


"""
Testat-API-Views
"""


class TestatListAPIViev(ListCreateAPIView):
    queryset = Testat.objects.all()
    serializer_class = TestatListSerializer
    filter_backends = [OrderingFilter]

    # support for multiple objects creation
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(TestatListAPIViev, self).get_serializer(*args, **kwargs)
