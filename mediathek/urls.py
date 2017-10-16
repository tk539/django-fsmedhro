from django.conf.urls import url
from . import views

app_name = 'mediathek'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^verwaltung/$', views.verwaltung, name='verwaltung'),
    url(r'^verwaltung/ausleihe$', views.ausleihe, name='ausleihe'),
]
