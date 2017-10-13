from django.conf.urls import url
from . import views

app_name = 'mediathek'
urlpatterns = [
    url(r'^$', views.mediathek_index, name='mediathek_index'),
    url(r'^verwaltung/$', views.mediathek_verwaltung, name='mediathek_verwaltung'),
    url(r'^verwaltung/ausleihe$', views.ausleihe, name='ausleihe'),
]
