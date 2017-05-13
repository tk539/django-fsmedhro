from django.conf.urls import url
from django.contrib import admin

from .views import (
    PrueferCreateAPIViev,
    PrueferListAPIView,
    PrueferDetailAPIViev,
    PrueferUpdateAPIViev,
    PrueferDeleteAPIViev,
    FrageListAPIViev,
    FrageDetailAPIViev,
    FrageDeleteAPIViev,
    FrageUpdateAPIViev,
)

urlpatterns = [
    url(r'^pruefer/$', PrueferListAPIView.as_view(), name='pruefer_list'),
    url(r'^pruefer/new/$', PrueferCreateAPIViev.as_view(), name='pruefer_new'),
    url(r'^pruefer/(?P<pk>\d+)/$', PrueferDetailAPIViev.as_view(), name='pruefer_detail'),
    url(r'^pruefer/(?P<pk>\d+)/edit/$', PrueferUpdateAPIViev.as_view(), name='pruefer_edit'),
    url(r'^pruefer/(?P<pk>\d+)/delete/$', PrueferDeleteAPIViev.as_view(), name='pruefer_delete'),
    url(r'^frage/$', FrageListAPIViev.as_view(), name='frage_list'),
    url(r'^frage/(?P<pk>\d+)/$', FrageDetailAPIViev.as_view(), name='frage_detail'),
    url(r'^frage/(?P<pk>\d+)/edit/$', FrageUpdateAPIViev.as_view(), name='frage_edit'),
    url(r'^frage/(?P<pk>\d+)/delete/$', FrageDeleteAPIViev.as_view(), name='frage_delete'),
]

#urlpatterns = router.urls
