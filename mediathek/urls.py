from django.conf.urls import url
from . import views

app_name = 'mediathek'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^bestellung_neu/(?P<sammelbest_id>[0-9]+)/$', views.sammelbest_auftrag_neu, name='sammelbest_auftrag_neu'),
    url(r'^bestellung/(?P<auftrag_id>[0-9]+)/$', views.sammelbest_auftrag_detail, name='sammelbest_auftrag_detail'),
]
