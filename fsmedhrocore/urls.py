from django.conf.urls import url
from fsmedhrocore.views import *

urlpatterns = [
    url(r'^user/(?P<username>[\w]+)/', user_profile, name='fsmedhro_user_profile'),
    url(r'^user/$', user_self_redirect, name='fsmedhro_user'),
    url(r'^user_new/', user_new, name='fsmedhro_user_new')
]
