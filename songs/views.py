from django.shortcuts import render

# Create your views here.

from songs.models import ServiceName, Song, BookName, ParshaName, TorahReading, HaftarahReading

# default, root view
def index(request):
    services = ServiceName.objects.all()
    return render(request, 'index.html', {'services': services})

# List of songs given a service name
def song_list(request, service_name):
    service = ServiceName.objects.get(pk=service_name)
    DUPLICATES = set()
    LIST = []
    songs = Song.objects.filter(service_name=service_name)
    for s in songs:
        if (s.name not in DUPLICATES):
            LIST.append(s)
            DUPLICATES.add(s.name)
    return render(request, 'song_list.html', {'songs': LIST, 'service': service})
