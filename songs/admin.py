from django.contrib import admin

from .models import ServiceName, Song, BookName, ParshaName, TorahReading, HaftarahReading

admin.site.register(ServiceName)
admin.site.register(Song)
admin.site.register(BookName)
admin.site.register(ParshaName)
admin.site.register(TorahReading)
admin.site.register(HaftarahReading)
