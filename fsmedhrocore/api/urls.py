from django.conf.urls import url
from .views import (
    StudienabschnittListAPIView,
    StudienabschnittDetailAPIView
    )


# api/fachschaft/...
urlpatterns = [
    url(r'^studienabschnitt/$',StudienabschnittListAPIView.as_view(), name='studienabschnitt_list'),
    url(r'^studienabschnitt/(?P<pk>[\d+])/$', StudienabschnittDetailAPIView.as_view(), name='studienabschnitt_detail'),
]