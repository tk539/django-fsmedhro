from django.conf.urls import url
from . import views

app_name = 'mediathek'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sammelbestellung/(?P<sammelbest_id>[0-9]+)/$', views.sammelbest_detail, name='sammelbest_detail'),
    url(r'^verwaltung/$', views.verwaltung, name='verwaltung'),
    url(r'^verwaltung/sammelbestellungen/$', views.sammelbest_list, name='sammelbest_list'),
    url(r'^verwaltung/ausleihe$', views.ausleihe, name='ausleihe'),
]
