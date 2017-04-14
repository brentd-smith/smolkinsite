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
    if service_type == 'TorahReading':
        return 'Torah Reading'
    elif service_type == 'HaftarahReading':
        return 'Haftarah Reading'
        
# get a list of all the parshas in a book of the Torah
def parsha_list(request, service_type, book_name):
    book = BookName.objects.get(pk=book_name)
    parshas = ParshaName.objects.filter(book_name=book_name)
    reading_type = get_reading_type(service_type)
    
    # filter the list so that the only parshas shown are those that actually have at least one reading
    if (service_type == 'HaftarahReading'):
        parshas = list(filter(lambda p: p.has_haftarah(), parshas))
    else:
        parshas = list(filter(lambda p: p.has_torah(), parshas))
    
    return render(request, 'parsha_list.html',
        {'parshas': parshas, 'book': book, 'reading_type': reading_type, 'service_type': service_type})


# get a list of all the readings available within a parsha
def reading_list(request, service_type, book_name, parsha_name):
    book = BookName.objects.get(pk=book_name)
    parsha = ParshaName.objects.get(pk=parsha_name)
    return render(request, 'reading_list.html',
        {'readings': parsha.reading_list, 'parsha': parsha, 'book': book})

# show the details of a torah reading, with all the audio files, lyric files, etc...
def torah_reading(request, service_type, book_name, parsha_name, triennial_cycle, aliyah):
    book = BookName.objects.get(pk=book_name)
    parsha = ParshaName.objects.get(pk=parsha_name)
    song = triennial_cycle + ' Triennial ' + aliyah + ' Aliyah'
    
    details = TorahReading.objects.filter(parsha=parsha_name, triennial=triennial_cycle, aliyah=aliyah)

    lyric_images = list(filter(is_jpg, details))
    audio_files = list(filter(is_mp3, details))
    lyric_doc = list(filter(is_pdf, details))
    
    reading_type = get_reading_type(service_type)
    return render(request, 'reading_detail.html',
        {'lyric_files': lyric_images, 'lyric_pages' : len(lyric_images),
        'audio_files': audio_files, 
        'lyric_doc': lyric_doc, 
        'song': song, 'parsha': parsha, 'book': book, 'reading_type': reading_type, 'service_type': service_type})
        

def haftarah_reading(request, service_type, book_name, parsha_name):
    book = BookName.objects.get(pk=book_name)
    parsha = ParshaName.objects.get(pk=parsha_name)
    song = parsha.display
    
    details = HaftarahReading.objects.filter(parsha=parsha_name)
    lyric_images = list(filter(is_jpg, details))
    audio_files = list(filter(is_mp3, details))
    lyric_doc = list(filter(is_pdf, details))
    
    reading_type = get_reading_type(service_type)
    
    return render(request, 'reading_detail.html',
        {
        'lyric_files': lyric_images, 'lyric_pages' : len(lyric_images),
        'audio_files': audio_files, 
        'lyric_doc': lyric_doc, 
        'song': song, 'parsha': parsha, 'book': book, 'reading_type': reading_type, 'service_type': service_type})