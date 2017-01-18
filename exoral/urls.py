from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^/$', views.moduswahl, name='exoral_moduswahl'),
    url(r'^(?P<modus>[lp])/$', views.testatwahl, name='exoral_testatwahl'),
    url(r'^(?P<modus>[lp])/(?P<testat_id>[0-9]+)/$', views.prueferwahl, name='exoral_prueferwahl'),
    url(r'^(?P<modus>[lp])/(?P<testat_id>[0-9]+)/(?P<pruefer_id>[0-9]+)/$', views.fragenliste,
        name='exoral_fragenliste'),
]
