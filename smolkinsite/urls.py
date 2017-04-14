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
    url(r'^service/(?P<service_name>[\-\'a-zA-Z]+)/$', songs.views.song_list),
    url(r'^service/(?P<service_name>[\-\'a-zA-Z]+)/(?P<song_name>[\-\'a-zA-Z]+)/$', songs.views.song_detail),

    # torah readings
    url(r'^(?P<service_type>torahreading)/$', songs.views.book_list),
    url(r'^(?P<service_type>torahreading)/(?P<book_name>[a-zA-Z]+)/$', songs.views.parsha_list),
    # url(r'(?P<service_type>trd)/(?P<book_name>[a-zA-Z]+)/(?P<parsha_name>[\-\'a-zA-Z]+)/(?P<triennial_cycle>1st|2nd|3rd)/(?P<aliyah>1st|2nd|3rd|4th|5th|6th|7th|Maftir)$', 
    #     songs.views.torah_reading, name='torah_reading'),
    # url(r'(?P<service_type>trd)/(?P<book_name>[a-zA-Z]+)/(?P<parsha_name>[\-\'a-zA-Z]+)', views.reading_list, name='reading_list'),
    # url(r'(?P<service_type>trd)/(?P<book_name>[a-zA-Z]+)', views.parsha_list, name='parsha_list'),

    
    # services
    # url(r'(?P<service_type>srv)/(?P<service_name>[\-\'a-zA-Z]+)', songs.views, name='songs'),
    # url(r'(?P<song_id>[0-9]+)/(?P<service_name>[\-\'a-zA-Z]+)/(?P<song_name>[a-zA-Z]+)', views.song_detail, name='song_detail'),   
]
