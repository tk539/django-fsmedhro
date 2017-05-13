from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework import viewsets

from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    ListCreateAPIView,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    IsAdminUser,
)

from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)

from exoral.models import (
    Pruefer,
    Frage,
)

from .serializers import (
    PrueferListSerializer,
    PrueferDetailSerializer,
    PrueferCreateUpdateSerializer,
    FrageListSerializer,
    FrageDetailSerializer,
    FrageUpdateSerializer,
)


"""
Prüfer-API-Views
"""
class PrueferCreateAPIViev(CreateAPIView):
    queryset = Pruefer.objects.all()
    serializer_class = PrueferCreateUpdateSerializer
    permission_classes = [IsAdminUser]


class PrueferDetailAPIViev(RetrieveAPIView):
    queryset = Pruefer.objects.all()
    serializer_class = PrueferDetailSerializer
    permission_classes = [IsAdminUser]


class PrueferUpdateAPIViev(RetrieveUpdateAPIView):
    queryset = Pruefer.objects.all()
    serializer_class = PrueferCreateUpdateSerializer
    permission_classes = [IsAdminUser]


class PrueferDeleteAPIViev(DestroyAPIView):
    queryset = Pruefer.objects.all()
    serializer_class = PrueferDetailSerializer
    permission_classes = [IsAdminUser]


class PrueferListAPIView(ListAPIView):
    queryset = Pruefer.objects.all()
    serializer_class = PrueferListSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['titel', 'nachname', 'vorname', 'fach__bezeichnung']
    pagination_class = LimitOffsetPagination #PageNumberPagination


"""
Frage-API-Views
"""
class FrageListAPIViev(ListCreateAPIView):
    queryset = Frage.objects.all()
    serializer_class = FrageListSerializer
    permission_classes = [IsAdminUser]
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
    permission_classes = [IsAdminUser]


class FrageDeleteAPIViev(DestroyAPIView):
    queryset = Frage.objects.all()
    serializer_class = FrageDetailSerializer
    permission_classes = [IsAdminUser]


class FrageUpdateAPIViev(RetrieveUpdateAPIView):
    queryset = Frage.objects.all()
    serializer_class = FrageUpdateSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user)


# TODO: Testate-List, Kommentare, Prüfer-Liste ausreichend ? (kein edit etc.)