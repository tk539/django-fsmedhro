from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from fsmedhrocore.models import (Studienabschnitt, Studiengang, Gender, FachschaftUser, Dozent, Fach)
from .serializers import StudienabschnittSerializer, FachListSerializer
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser, DjangoModelPermissions)
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

class StudienabschnittListAPIView(ListAPIView):
    queryset = Studienabschnitt.objects.all()
    serializer_class = StudienabschnittSerializer
    permission_classes = [IsAdminUser]


class StudienabschnittDetailAPIView(RetrieveAPIView):
    queryset = Studienabschnitt.objects.all()
    serializer_class = StudienabschnittSerializer
    permission_classes = [IsAdminUser]


"""
Fach-API-Views
"""


class FachListAPIViev(ListCreateAPIView):
    queryset = Fach.objects.all()
    serializer_class = FachListSerializer
    permission_classes = [DjangoModelPermissions]
    filter_backends = [OrderingFilter]

    # support for multiple objects creation
    def get_serializer(self, *args, **kwargs):
        """ if an array is passed, set serializer to many """
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super(FachListAPIViev, self).get_serializer(*args, **kwargs)