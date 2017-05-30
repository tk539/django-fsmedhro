"""fsmedhro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.conf import settings
from django.conf.urls.static import static
from wiki.urls import get_pattern as get_wiki_pattern
from django_nyt.urls import get_pattern as get_nyt_pattern
#  from django.views.generic import RedirectView


urlpatterns = [
    #url(r'^$', RedirectView.as_view(url='https://fachschaft-medizin-rostock.de/'), name='root'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', login, {'template_name': 'login.html'}, name='fsmedhro_login'),
    url(r'^logout/$', logout, {'template_name': 'logout.html'}, name='fsmedhro_logout'),
    url(r'^fachschaft/', include('fsmedhrocore.urls')),
    url(r'^exoral/', include('exoral.urls')),
    url(r'^api/fachschaft/', include('fsmedhrocore.api.urls', namespace='fsmedhrocore-api')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^cms-forms/', include('djangocms_forms.urls')),
    url(r'^data/', include('filer.urls')),
    url(r'^notifications/', get_nyt_pattern()),
    url(r'^pharos/', get_wiki_pattern()),
    url(r'^', include('cms.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
