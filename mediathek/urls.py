from django.conf.urls import url
from . import views

app_name = 'mediathek'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^verwaltung/$', views.verwaltung, name='verwaltung'),
    url(r'^verwaltung/sammelbestellung/$', views.sammelbest_list, name='sammelbest_list'),
    url(r'^verwaltung/sammelbestellung/(?P<sammelbest_id>[0-9]+)/$', views.sammelbest_detail, name='sammelbest_detail'),
    url(r'^verwaltung/ware/$', views.waren_list, name='waren_list'),
    url(r'^verwaltung/ware/(?P<ware_id>[0-9]+)/$', views.ware_detail, name='ware_detail'),
    url(r'^verwaltung/ausleihe$', views.ausleihe, name='ausleihe'),
]
