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

def is_jpg(x): return x.extension == "jpg"
def is_pdf(x): return x.extension == "pdf" 
def is_mp3(x): return x.extension == "mp3"

def song_detail(request, service_name, song_name):
    details = Song.objects.filter(name=song_name)
    service = ServiceName.objects.get(pk=service_name)
    
    lyric_images = list(filter(is_jpg, details))
    audio_files = list(filter(is_mp3, details))
    lyric_doc = list(filter(is_pdf, details))

    return render(request, 'song_detail.html',
        {'lyric_files': lyric_images, 
        'audio_files': audio_files, 
        'lyric_doc': lyric_doc, 
        'song': details[0],
        'service': service
        })

# get a list of all the books of the Torah
def book_list(request, service_type):
    books = BookName.objects.all()
    return render(request, 'book_list.html', {'books': books, 'service_type': service_type})
    

def get_reading_type(service_type):
    if service_type == 'torahreading':
        return 'Torah Reading'
    elif service_type == 'haftarahreading':
        return 'Haftarah Reading'
        

# get a list of all the parshas in a book of the Torah
def parsha_list(request, service_type, book_name):
    book = BookName.objects.get(pk=book_name)
    parshas = ParshaName.objects.filter(book_name=book_name)
    reading_type = get_reading_type(service_type)
    # if (service_type == 'haftarahreading'):
    #     parshas = filter(has_haftarah, parshas)
    return render(request, 'parsha_list.html',
        {'parshas': parshas, 'book': book, 'reading_type': reading_type, 'service_type': service_type})

