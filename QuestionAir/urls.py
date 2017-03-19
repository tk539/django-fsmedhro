from django.conf.urls import url
from . import views

app_name = 'QuestionAir'
urlpatterns = [
    url(r'^$', views.fachwahl, name='Fächerwahl'),
    url(r'(?P<fach_id>[0-9]+)/$', views.klausurwahl, name='Klausurwahl'),
]
#TODO: complete