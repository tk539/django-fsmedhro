from django.conf.urls import url
from . import views

app_name = 'exoral'
urlpatterns = [
    url(r'^$', views.moduswahl, name='moduswahl'),
    url(r'^(?P<modus>[lp])/$', views.testatwahl, name='testatwahl'),
    url(r'^(?P<modus>[lp])/(?P<testat_id>[0-9]+)/$', views.prueferwahl, name='prueferwahl'),
    url(r'^(?P<modus>[lp])/(?P<testat_id>[0-9]+)/(?P<pruefer_id>[0-9]+)/$', views.fragenliste,
        name='fragenliste'),
    url(r'^(?P<modus>[lp])/(?P<testat_id>[0-9]+)/(?P<pruefer_id>[0-9]+)/frage_neu/$', views.frage_neu,
        name='frage_neu'),
]
