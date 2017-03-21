from rest_framework.generics import ListAPIView, RetrieveAPIView
from fsmedhrocore.models import (Studienabschnitt, Studiengang, Gender, FachschaftUser, Dozent)
from .serializers import StudienabschnittSerializer
from rest_framework.permissions import (AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser)


class StudienabschnittListAPIView(ListAPIView):
    queryset = Studienabschnitt.objects.all()
    serializer_class = StudienabschnittSerializer
    permission_classes = [IsAdminUser]


class StudienabschnittDetailAPIView(RetrieveAPIView):
    queryset = Studienabschnitt.objects.all()
    serializer_class = StudienabschnittSerializer
    permission_classes = [IsAdminUser]