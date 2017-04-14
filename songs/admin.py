from django.contrib import admin

from .models import ServiceName, Song, BookName, ParshaName, TorahReading, HaftarahReading

# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email')

class ServiceNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'seq_number')
    ordering = ('seq_number',)

admin.site.register(ServiceName, ServiceNameAdmin)

class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'seq_number', 's3_obj_key', 'file_name')
    ordering = ('seq_number',)
    list_filter = ('service_name',)

admin.site.register(Song, SongAdmin)

class BookNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'seq_number')
    ordering = ('seq_number',)

admin.site.register(BookName, BookNameAdmin)


class ParshaNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'display', 'seq_number')
    ordering = ('seq_number',)
    list_filter = ('book_name',)

admin.site.register(ParshaName, ParshaNameAdmin)

class TorahReadingAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'triennial', 'aliyah', 'extension', 'seq_number', 's3_obj_key')
    ordering = ('seq_number',)
    search_fields = ('file_name', 'triennial', 'aliyah',)
    list_filter = ('parsha',)

admin.site.register(TorahReading, TorahReadingAdmin)

class HaftarahReadingAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'extension', 'seq_number', 's3_obj_key')
    ordering = ('seq_number',)
    search_fields = ('file_name',)

admin.site.register(HaftarahReading, HaftarahReadingAdmin)
