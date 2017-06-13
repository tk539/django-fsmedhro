from django.conf.urls import url

from .views import (
    FrageListAPIViev,
    FrageDetailAPIViev,
    FrageDeleteAPIViev,
    FrageUpdateAPIViev,
    KommentarListAPIViev,
    KommentarDetailAPIViev,
    KommentarDeleteAPIViev,
    KommentarUpdateAPIViev,
    ProtokollListAPIViev,
    ProtokollDetailAPIViev,
    ProtokollDeleteAPIViev,
    ProtokollUpdateAPIViev,
    PrueferListAPIView,
    TestatListAPIViev,
)

urlpatterns = [
    url(r'^frage/$', FrageListAPIViev.as_view(), name='frage_list'),
    url(r'^frage/(?P<pk>\d+)/$', FrageDetailAPIViev.as_view(), name='frage_detail'),
    url(r'^frage/(?P<pk>\d+)/edit/$', FrageUpdateAPIViev.as_view(), name='frage_edit'),
    url(r'^frage/(?P<pk>\d+)/delete/$', FrageDeleteAPIViev.as_view(), name='frage_delete'),
    url(r'^kommentar/$', KommentarListAPIViev.as_view(), name='kommentar_list'),
    url(r'^kommentar/(?P<pk>\d+)/$', KommentarDetailAPIViev.as_view(), name='kommentar_detail'),
    url(r'^kommentar/(?P<pk>\d+)/edit/$', KommentarUpdateAPIViev.as_view(), name='kommentar_edit'),
    url(r'^kommentar/(?P<pk>\d+)/delete/$', KommentarDeleteAPIViev.as_view(), name='kommentar_delete'),
    url(r'^protokoll/$', ProtokollListAPIViev.as_view(), name='protokoll_list'),
    url(r'^protokoll/(?P<pk>\d+)/$', ProtokollDetailAPIViev.as_view(), name='protokoll_detail'),
    url(r'^protokoll/(?P<pk>\d+)/edit/$', ProtokollUpdateAPIViev.as_view(), name='protokoll_edit'),
    url(r'^protokoll/(?P<pk>\d+)/delete/$', ProtokollDeleteAPIViev.as_view(), name='protokoll_delete'),
    url(r'^pruefer/$', PrueferListAPIView.as_view(), name='pruefer_list'),
    url(r'^testat/$', TestatListAPIViev.as_view(), name='testat_list'),
]

#urlpatterns = router.urls
