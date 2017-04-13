"""smolkinsite URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
import songs.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', songs.views.index),
    url(r'^service/(?P<service_name>[\-\'a-zA-Z]+)', songs.views.song_list)
    
    # services
    # url(r'(?P<service_type>srv)/(?P<service_name>[\-\'a-zA-Z]+)', songs.views, name='songs'),
    # url(r'(?P<song_id>[0-9]+)/(?P<service_name>[\-\'a-zA-Z]+)/(?P<song_name>[a-zA-Z]+)', views.song_detail, name='song_detail'),   
]
