from django.conf.urls import url
from fsmedhrocore import views

urlpatterns = [
    url(r'^$', views.fachschaft_index, name='fsmedhro_index'),
    url(r'^user/(?P<username>[\w]+)/', views.user_profile, name='fsmedhro_user_profile'),
    url(r'^user/$', views.user_self_redirect, name='fsmedhro_user'),
    url(r'^user_edit/$', views.user_edit, name='fsmedhro_user_edit'),
]

# TODO: erstes Mal user_edit, danach zurück zu z.B. exoral (GET "next" in user_edit verwenden)