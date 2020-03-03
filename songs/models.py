from __future__ import unicode_literals
from django.db import models

import datetime
from django.utils import timezone

READING_TYPES = ((None, None),
    ('Torah', 'Torah'),
    ('Haftarah', 'Haftarah'),
    )

TRIENNIALS = (
    (None, None),
    ('1st', '1st Triennial'),
    ('2nd', '2nd Triennial'),
    ('3rd', '3rd Triennial'),
    )

ALIYAHS = (
    (None, None),
    ('1st', '1st Aliyah'),
    ('2nd', '2nd Aliyah'),
    ('3rd', '3rd Aliyah'),
    ('4th', '4th Aliyah'),
    ('5th', '5th Aliyah'),
    ('6th', '6th Aliyah'),
    ('7th', '7th Aliyah'),
    ('Maftir', 'Maftir'),
    )

# ------------------------------------------------------------------------------
# Models version 2
# ------------------------------------------------------------------------------

MP3 = "mp3"
PDF = "pdf"
JPG = "jpg"
PNG = "png"
EXTENSIONS = ((MP3, MP3), (PDF, PDF), (JPG, JPG), (PNG, PNG))


# Represents one of the services at OZS
class ServiceName(models.Model):

    # The name of the Service, ex: "KabbalatShabbat"
    name = models.CharField(max_length=64, primary_key=True)

    # More descriptive name, ex: "Kabbalat Shabbat"
    display = models.CharField(max_length=64, null=False)
    
    # Sequence Number/Sort Order for display in web site
    seq_number = models.PositiveSmallIntegerField(null=False)
    
    def __str__(self):
        return self.display


# Represents a Song or melody sung at one of the services
class Song(models.Model):
    
    # FK to the ServiceName class, each Service can have 1 or more songs
    service_name = models.ForeignKey(ServiceName, on_delete=models.CASCADE)
    
    # The name of the Song, ex: "ShalomAlechem"
    name = models.CharField(max_length=128, null=False)
    
    # More descriptive name of the song, ex: "Shalom Alechem"
    display = models.CharField(max_length=128, null=False)
    
    # Object Key to the object stored within S3, prepend the bucket name 
    s3_obj_key = models.CharField(max_length=2048, null=False)
    
    # The 3 character extension of the file
    extension = models.CharField(max_length=3, choices=EXTENSIONS, default=MP3)
    
    # Page number correspoding to the page of the song located in Or Chadash Siddur
    page_number = models.PositiveSmallIntegerField(null=False)
    
    # Sequence Number/Sort Order number to indicate way to sort the info on the website.
    seq_number = models.PositiveSmallIntegerField(null=False)
    
    # File name of the specific file plus extension, ex: "Shalom Alechem A.mp3"
    file_name = models.CharField(max_length=128, null=False)
    
    def __str__(self):
        return self.display


# 07 - Torah Readings/01 - Breshit (Genesis)/02 Parshat Noach/3rd Triennial Noach 6th Aliyah/3rd Triennial Noach 6th Aliyah-0.jpg
# 07 - Torah Readings/01 - Breshit (Genesis)/02 Parshat Noach/3rd Triennial Noach 6th Aliyah/3rd Triennial Noach 6th Aliyah-1.jpg
# 07 - Torah Readings/01 - Breshit (Genesis)/02 Parshat Noach/3rd Triennial Noach 6th Aliyah/3rd Triennial Noach 6th Aliyah.mp3
# 07 - Torah Readings/01 - Breshit (Genesis)/02 Parshat Noach/3rd Triennial Noach 6th Aliyah/3rd Triennial Noach 6th Aliyah.pdf

# Represents a Book of the TaNaKh, ex: Breshit (Genesis)
class BookName(models.Model):

    # The name of the Book, ex: "Breshit"
    name = models.CharField(max_length=64, primary_key=True)

    # More descriptive name, ex: "Breshit (Genesis)"
    display = models.CharField(max_length=64, null=False)
    
    # Sequence Number/Sort Order for display in web site
    seq_number = models.PositiveSmallIntegerField(null=False)

    def __str__(self):
        return self.display
    
    # Suitable for use in an S3 object key 01 - Breshit (Genesis)   
    def object_key(self):
        return "%02d - %s" % (self.seq_number, self.display)

class AlternateBookName(models.Model):
    
    # FK to the BookName
    book_name = models.ForeignKey(BookName)

    # Comma separated list of potential alternate parsha names
    # Example 'Vayirka, Vayeekra' or whatever
    # During an input/load of new data, if parsha name not found, look for it here....
    alternate_name = models.CharField(max_length=256,null=True)
   


# Represents a Parsha from one of the books of the Torah
class ParshaName(models.Model):

    # FK to the BookName class, each book has 1-N Parshas
    book_name = models.ForeignKey(BookName, on_delete=models.CASCADE)

    # The name of the Parsha, ex: "Vayikra"
    name = models.CharField(max_length=64, primary_key=True)

    # More descriptive name, ex: "Parshat Vayikra"
    display = models.CharField(max_length=64, null=False)
    
    # Sequence Number/Sort Order for display in web site
    seq_number = models.PositiveSmallIntegerField(null=False)

    # Sequence Number that is prepended to the display name as part of the object key
    prefix = models.CharField(max_length=4,null=False)
    
    # check to see if there is a haftarah reading present for this parsha
    def has_haftarah(self):
        readings = HaftarahReading.objects.filter(parsha=self.name)
        return len(readings) > 0
        
    # check to see if there is a torah reading present for this parsha
    def has_torah(self):
        readings = TorahReading.objects.filter(parsha=self.name)
        return len(readings) > 0
        
    # get a count of the number of torah readings there are within a parsha
    def reading_count(self):
        DUPLICATES = []
        LIST = []
        readings = TorahReading.objects.filter(parsha=self.name)
        for s in readings:
            if DUPLICATES.count(s.display()) == 0:
                LIST.append(s)
                DUPLICATES.append(s.display())
        return len(LIST)
                
    # get a list of the unique torah reading names with a parsha
    def reading_list(self):
        DUPLICATES = []
        LIST = []
        readings = TorahReading.objects.filter(parsha=self.name).order_by('file_name')
        for s in readings:
            if DUPLICATES.count(s.display()) == 0:
                LIST.append(s)
                DUPLICATES.append(s.display())
        return LIST
        
    def __str__(self):
        return self.display
        
    # Suitable for use in an S3 object key 01 Parshat Vayikra
    def object_key(self):
        return "%s %s" % (self.prefix, self.display)


class AlternateParshaName(models.Model):
    
    # FK to the ParshaName
    parsha_name = models.ForeignKey(ParshaName)

    # Comma separated list of potential alternate parsha names
    # Example 'Vayirka, Vayeekra' or whatever
    # During an input/load of new data, if parsha name not found, look for it here....
    alternate_name = models.CharField(max_length=256,null=True)
   

# Represents a Reading - Either a Torah Reading or a Haftarah Reading
class TorahReading(models.Model):
    
    # The Book of the TaNaKh where the reading comes from, ex: Breshit (Genesis)
    # book = models.CharField(max_length=128, null=False)
    
    # The Parsha (section) where the reading comes from, ex: Parshat Noach
    parsha = models.ForeignKey(ParshaName, on_delete=models.CASCADE)
    
    # Triennial Year cycle of readings - either 1st, 2nd, or 3rd
    triennial = models.CharField(max_length=3, choices=TRIENNIALS, default='1st')
    
    # Aliyah - typically there are 7 + the Maftir reading for each Parsha
    aliyah = models.CharField(max_length=6, choices=ALIYAHS, default='1st')

    # The 3 character extension of the file
    extension = models.CharField(max_length=3, choices=EXTENSIONS, default=MP3)
    
    # Object Key to the object stored within S3, prepend the bucket name 
    s3_obj_key = models.CharField(max_length=2048, null=False)

    # Sequence Number/Sort Order number to indicate way to sort the info on the website.
    seq_number = models.PositiveSmallIntegerField(null=False)
    
    # File name of the specific file plus extension, ex: "3rd Triennial Noach 6th Aliyah.pdf"
    file_name = models.CharField(max_length=128, null=False)

    def display(self):
        return self.triennial + ' Triennial ' + self.aliyah + ' Aliyah'
    
    def __str__(self):
        return self.triennial + ' Triennial ' + self.aliyah + ' Aliyah'



# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Haftarah for Ki Tetzei - Hebrew-0.jpg
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Haftarah for Ki Tetzei - Hebrew-1.jpg
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Haftarah for Ki Tetzei - Hebrew.pdf
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Haftarah for Ki Tetzei.mp3
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Isa 54-1.mp3
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Isa 54-10.mp3
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Isa 54-2.mp3

# Represents a Haftarah Reading from one of the Prophetic book within the TaNaKh
class HaftarahReading(models.Model):
    
    # The Book of the TaNaKh where the reading comes from, ex: Breshit (Genesis)
    # book = models.CharField(max_length=128, null=False)
    
    # The Parsha (section) where the reading comes from, ex: Parshat Noach
    parsha = models.ForeignKey(ParshaName, on_delete=models.CASCADE)

    # The 3 character extension of the file
    extension = models.CharField(max_length=3, choices=EXTENSIONS, default=MP3)
    
    # Object Key to the object stored within S3, prepend the bucket name 
    s3_obj_key = models.CharField(max_length=2048, null=False)

    # Sequence Number/Sort Order number to indicate way to sort the info on the website.
    seq_number = models.PositiveSmallIntegerField(null=False)
    
    # File name of the specific file plus extension, ex: "3rd Triennial Noach 6th Aliyah.pdf"
    file_name = models.CharField(max_length=128, null=False)

    def display(self):
        return 'Haftarah for ' + self.parsha.display
    
    def __str__(self):
        return 'Haftarah for ' + self.parsha.display
        

# For uploading documents
class Document(models.Model):
    
    # Description is a required field
    description = models.CharField(max_length=255)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
