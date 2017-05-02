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
from django.conf import settings
from django.conf.urls.static import static

import songs.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', songs.views.index),
    url(r'^ServiceName/(?P<service_name>[\-\'a-zA-Z]+)/$', songs.views.song_list),
    url(r'^ServiceName/(?P<service_name>[\-\'a-zA-Z]+)/(?P<song_name>[\-\'a-zA-Z]+)/$', songs.views.song_detail),

    # torah readings
    url(r'^(?P<service_type>TorahReading)/$', songs.views.book_list),
    url(r'^(?P<service_type>TorahReading)/(?P<book_name>[a-zA-Z]+)/$', songs.views.parsha_list),
    url(r'(?P<service_type>TorahReading)/(?P<book_name>[a-zA-Z]+)/(?P<parsha_name>[\-\'a-zA-Z]+)/$', songs.views.reading_list),
    url(r'(?P<service_type>TorahReading)/(?P<book_name>[a-zA-Z]+)/(?P<parsha_name>[\-\'a-zA-Z]+)/(?P<triennial_cycle>1st|2nd|3rd)/(?P<aliyah>1st|2nd|3rd|4th|5th|6th|7th|Maftir)$', songs.views.torah_reading),

    # haftarah readings
    url(r'(?P<service_type>HaftarahReading)/$', songs.views.book_list),
    url(r'(?P<service_type>HaftarahReading)/(?P<book_name>[a-zA-Z]+)/$', songs.views.parsha_list),
    url(r'(?P<service_type>HaftarahReading)/(?P<book_name>[a-zA-Z]+)/(?P<parsha_name>[\-\'a-zA-Z]+)/$', songs.views.haftarah_reading),
    
    # uploading files
    url(r'^docs/$', songs.views.document_list),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

