import argparse
import fileinput
import re
import sys
import os.path
from songs.models import BookName, ParshaName, TorahReading
from songs.models import ServiceName

# '1st Triennial Ki Tisa 2nd Aliyah'
PARSERS = { 
    'dir': r"^(\d+.?\d*)?\s?[A|B]?\s?-?\s?([a-zA-Z_\s\W\d]+)",  # directory name and sort order
    'parsha': r"^\d{2}.?\d?\sParshat\s(.+)$",                 # parsha name
    'tri': r"^(1st|2nd|3rd)\sTriennial\s.+(1st|2nd|3rd|4th|5th|6th|7th|Maftir)",   #group1 = Triennial Cycle, group2 = Aliyah
    'file': r"^(1st|2nd|3rd)\sTriennial\s(.+)(1st|2nd|3rd|4th|5th|6th|7th|Maftir)",   #group1 = Triennial Cycle, group2 = Parsha, group3 = Aliyah
}

ROOTS = set()
DIRECTORIES = set()

valid_dir_name = re.compile(PARSERS['dir'])
valid_parsha_name = re.compile(PARSERS['parsha'])
valid_tri_name = re.compile(PARSERS['tri'])
valid_from_file_name = re.compile(PARSERS['file'])

# filename: 3rd Triennial Noach 6th Aliyah.pdf
# returns:  07 - Torah Readings/01 - Breshit (Genesis)/02 Parshat Noach/3rd Triennial Noach 6th Aliyah/
def get_object_key(filename, debug=True):
    """
    Given a file name, will determine the S3 object key that is expected for that file. Should be
    handed a filename with the full information on it such as "3rd Triennial Noach 6th Aliyah.pdf".
    """
    
    (f, ext) = os.path.splitext(filename)
    
    triennial = valid_from_file_name.match(filename).group(1)
    parsha_name = valid_from_file_name.match(filename).group(2)
    parsha_name = parsha_name.replace(' ', '')
    aliyah = valid_from_file_name.match(filename).group(3)
    Parsha = ParshaName.objects.all().get(pk=parsha_name)
    Book = ParshaName.objects.all().filter(name=parsha_name)[0].book_name
    the_s3_object_key = os.path.join("07 - Torah Readings", Book.object_key(), Parsha.object_key(), f)
    
    if (debug): 
        print("ParshaName={}".format(parsha_name))
        print("Aliah={}".format(aliyah))
        print("Triennial={}".format(triennial))
        print("BookName={}".format(Book.name))
        print("Root Service Name={}".format("07 - Torah Readings"))
        print("S3 Object Key = {}".format(the_s3_object_key))
        
    return the_s3_object_key


# 07 - Torah Readings/01 - Breshit (Genesis)/02 Parshat Noach/3rd Triennial Noach 6th Aliyah/3rd Triennial Noach 6th Aliyah.pdf
def process_one_line(line, count, debug=True):

    line = line.rstrip("\n\r")
    line = line.rstrip('/')
    folders = line.split('/')
    if len(folders) == 5:
        if (debug): 
            print('s3_obj_key=', line)
            print('folders=', folders)
        
        book_folder = folders[1]
        if (debug): print('BookFolder=', book_folder)
        
        bs = book_folder.split(' ')
        book_name = bs[2]
        if (debug): print('BookName=', book_name)
        bk = BookName.objects.get(pk=book_name)
        
        parsha_folder = folders[2]
        # ps = parsha_folder.split(' ')
        # service_name = valid_dir_name.match(service_folder).group(2)
        parsha_name = valid_parsha_name.match(parsha_folder).group(1)
        parsha_name = parsha_name.replace(" ", "")
        if (debug): print('ParshaName=', parsha_name)
        psh = ParshaName.objects.get(pk=parsha_name)

        tri_folder = folders[3]
        tri = valid_tri_name.match(tri_folder).group(1)
        if (debug): print('tri cycle=',tri)
        al = valid_tri_name.match(tri_folder).group(2)
        if (debug): print('aliyah=',al)
        
        file_name = folders[4]
        if (debug): print('FileName=',file_name)
        
        # Figure out the extension
        ext=''
        if file_name.lower().endswith(".mp3") :
            ext = "mp3"
        elif file_name.lower().endswith(".pdf") :
            ext = "pdf"
        elif file_name.lower().endswith(".jpg") :
            ext = "jpg"
        if (debug): 
            print('Extension=',ext)
        
        # # The Parsha (section) where the reading comes from, ex: Parshat Noach
        # parsha = models.ForeignKey(ParshaName, on_delete=models.CASCADE)
        
        # # Triennial Year cycle of readings - either 1st, 2nd, or 3rd
        # triennial = models.CharField(max_length=3, choices=TRIENNIALS, default='1st')
        
        # # Aliyah - typically there are 7 + the Maftir reading for each Parsha
        # aliyah = models.CharField(max_length=3, choices=ALIYAHS, default='1st')
    
        # # The 3 character extension of the file
        # extension = models.CharField(max_length=3, choices=EXTENSIONS, default=MP3)
        
        # # Object Key to the object stored within S3, prepend the bucket name 
        # s3_obj_key = models.CharField(max_length=2048, null=False)
    
        # # Sequence Number/Sort Order number to indicate way to sort the info on the website.
        # seq_number = models.PositiveSmallIntegerField(null=False)
        
        # # File name of the specific file plus extension, ex: "3rd Triennial Noach 6th Aliyah.pdf"
        # file_name = models.CharField(max_length=128, null=False)

        if (not debug):
            tr = TorahReading(
                parsha=psh,
                triennial=tri,
                aliyah=al,
                extension=ext,
                s3_obj_key=line,
                seq_number=count,
                file_name=file_name
                )
            tr.save()
        
        # sg = Song(
        #     service_name=srv, 
        #     name=song_name.replace(" ", ""), 
        #     display=song_name, 
        #     s3_obj_key=line, 
        #     extension=ext, 
        #     page_number=page_number, 
        #     seq_number=page_number,
        #     file_name=file_name)
        # sg.save()
        
        if (debug): print('sequence number = ', count)
# end process_one_line

def build_db_from_text(fh, clear=True):
    try:
        
        if clear:
            addBooksAndParshas()
            
            torah = TorahReading.objects.all()
            torah.delete()



        line_count = 0
        for line in fh:
            process_one_line(line, line_count, debug=False)
            line_count += 1
        fh.close()
    except:
        # print(line_count, line
        print("Something bad happened:", sys.exc_info()[0])
        fh.close()
        raise
# end build_db_from_text

def text2db(file_name='torah_readings.txt', clear=True):
    build_db_from_text(fileinput.input(file_name), clear)
# end text2db


def addBooksAndParshas():
    """
    Clear the database by deleting all currently added Books and Parshas. Then
    add all books and parshas to the database.
    """
    print("loading books and parshas...")
    
    book_names = BookName.objects.all()
    book_names.delete()
    
    parshas = ParshaName.objects.all()
    parshas.delete()
    
    # add books            
    breshit = BookName(name='Breshit', display='Breshit (Genesis)', seq_number=1)
    breshit.save()
    
    shemot = BookName("Shemot", "Shemot (Exodus)", 2)
    shemot.save()
    
    vayikra = BookName("Vayikra", "Vayikra (Leviticus)", 3)
    vayikra.save()
    
    bemidbar = BookName("Bemidbar", "Bemidbar (Numbers)", 4)
    bemidbar.save()
    
    devarim = BookName("Devarim", "Devarim (Deuteronomy)", 5)
    devarim.save()
    
    breshit = BookName.objects.get(pk='Breshit')
    shemot = BookName.objects.get(pk='Shemot')
    vayikra = BookName.objects.get(pk='Vayikra')
    bemidbar = BookName.objects.get(pk='Bemidbar')
    devarim = BookName.objects.get(pk='Devarim')
    
    # add parshas
    psh = ParshaName(book_name=breshit, name='Breshit', display='Parshat Breshit',seq_number=1, prefix="01")
    psh.save()
    
    # verify the foreign key is working as expected
    # tmp1 = ParshaName.objects.get(pk='Breshit')
    # print(tmp1.name, tmp1.display)
    # print(tmp1.book_name.name)
    
    psh = ParshaName(book_name=breshit, name='Noach', display='Parshat Noach',seq_number=2, prefix="02")
    psh.save()
    
    psh = ParshaName(book_name=breshit, name='LechLecha', display='Parshat Lech Lecha',seq_number=3, prefix="03")
    psh.save()
    
    psh = ParshaName(book_name=breshit, name='Vayera', display='Parshat Vayera',seq_number=4, prefix="04")
    psh.save()
    
    psh = ParshaName(book_name=breshit, name='ChayeSarah', display='Parshat Chaye Sarah',seq_number=5, prefix="05")
    psh.save()
    
    psh = ParshaName(book_name=breshit, name='Toldot', display='Parshat Toldot',seq_number=6, prefix="06")
    psh.save()
    
    psh = ParshaName(book_name=breshit, name='Vayetze', display='Parshat Vayetze',seq_number=7, prefix="07")
    psh.save()
    
    psh = ParshaName(book_name=breshit, name='Vayishlach', display='Parshat Vayishlach',seq_number=8, prefix="08")
    psh.save()
    
    psh = ParshaName(book_name=breshit, name='Vayeshev', display='Parshat Vayeshev',seq_number=9, prefix="09")
    psh.save()
    
    psh = ParshaName(book_name=breshit, name='Mikeitz', display='Parshat Mikeitz',seq_number=10, prefix="10")
    psh.save()
    
    psh = ParshaName(book_name=breshit, name='Vayigash', display='Parshat Vayigash',seq_number=11, prefix="11")
    psh.save()
    
    psh = ParshaName(book_name=breshit, name='Vayechi', display='Parshat Vayechi',seq_number=12, prefix="12")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name='Shemot', display='Parshat Shemot',seq_number=13, prefix="01")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name="Va'eira",display="Parshat Va'eira",seq_number=14,prefix="02")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name='Bo', display='Parshat Bo',seq_number=15,prefix="03")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name='Beshalach', display='Parshat Beshalach',seq_number=16, prefix="04")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name='Yitro', display='Parshat Yitro',seq_number=17, prefix="05")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name='Mishpatim', display='Parshat Mishpatim',seq_number=18, prefix="06")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name='Trumah', display='Parshat Trumah',seq_number=19, prefix="07")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name="T'tzaveh",display="Parshat T'tzaveh",seq_number=20, prefix="08")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name='KiTisa', display='Parshat Ki Tisa',seq_number=21, prefix="09")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name='Vayakhel', display='Parshat Vayakhel',seq_number=22, prefix="10")
    psh.save()
    
    psh = ParshaName(book_name=shemot, name='Pekudei', display='Parshat Pekudei',seq_number=23, prefix="11")
    psh.save()
    
    psh = ParshaName(book_name=vayikra, name='Vayikra', display='Parshat Vayikra',seq_number=24, prefix="01")
    psh.save()
    
    psh = ParshaName(book_name=vayikra, name='Tzav', display='Parshat Tzav',seq_number=25, prefix="02")
    psh.save()
    
    psh = ParshaName(book_name=vayikra, name='Shemini', display='Parshat Shemini',seq_number=26, prefix="03")
    psh.save()
    
    psh = ParshaName(book_name=vayikra, name='Tazria-Metzora', display='Parshat Tazria-Metzora',seq_number=27, prefix="04.5")
    psh.save()
    
    psh = ParshaName(book_name=vayikra, name='Metzora', display='Parshat Metzora',seq_number=28, prefix="05")
    psh.save()
    
    psh = ParshaName(book_name=vayikra, name='AchareiMot-Kedoshim', display='Parshat Acharei Mot-Kedoshim',seq_number=29, prefix="06.5")
    psh.save()
    
    psh = ParshaName(book_name=vayikra, name='Emor', display='Parshat Emor',seq_number=30, prefix="08")
    psh.save()
    
    psh = ParshaName(book_name=vayikra, name='Behar', display='Parshat Behar',seq_number=31, prefix="09")
    psh.save()
    
    psh = ParshaName(book_name=vayikra, name='Behar-Bechukotai', display='Parshat Behar - Bechukotai',seq_number=32, prefix="09.5")
    psh.save()
    
    psh = ParshaName(book_name=vayikra, name='Bechukotai', display='Parshat Bechukotai',seq_number=33, prefix="10")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='Bemidbar', display='Parshat Bemidbar',seq_number=34, prefix="01")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='Naso', display='Parshat Naso',seq_number=35, prefix="02")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='Behaalotcha', display='Parshat Behaalotcha',seq_number=36, prefix="03")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='Shelach', display='Parshat Shelach',seq_number=37, prefix="03")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='ShlachLecha', display='Parshat Shlach Lecha', seq_number=37, prefix="04")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='Korach', display='Parshat Korach',seq_number=38, prefix="05")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='Chukat', display='Parshat Chukat',seq_number=39, prefix="06")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='Balak', display='Parshat Balak',seq_number=40, prefix="07")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='Pinchas', display='Parshat Pinchas',seq_number=41, prefix="08")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='Matot', display='Parshat Matot',seq_number=42, prefix="09")
    psh.save()
    
    psh = ParshaName(book_name=bemidbar, name='Massei', display='Parshat Massei',seq_number=43, prefix="10")
    psh.save()
    
    psh = ParshaName(book_name=devarim, name='Devarim', display='Parshat Devarim',seq_number=44, prefix="01")
    psh.save()
    
    psh = ParshaName(book_name=devarim, name='Eikev', display='Parshat Eikev',seq_number=45, prefix="03")
    psh.save()
    
    psh = ParshaName(book_name=devarim, name="R'eh",display="Parshat R'eh",seq_number=46, prefix="04")
    psh.save()
    
    psh = ParshaName(book_name=devarim, name='Shoftim', display='Parshat Shoftim',seq_number=47, prefix="05")
    psh.save()
    
    psh = ParshaName(book_name=devarim, name='KiTetze', display='Parshat Ki Tetze',seq_number=48, prefix="06")
    psh.save()
    
    psh = ParshaName(book_name=devarim, name='KiTavo', display='Parshat Ki Tavo',seq_number=49, prefix="07")
    psh.save()
    
    psh = ParshaName(book_name=devarim, name='NitzavimVayelech', display='Parshat Nitzavim Vayelech',seq_number=50, prefix="08")
    psh.save()
    
    psh = ParshaName(book_name=devarim, name='Vayelech', display='Parshat Vayelech',seq_number=51, prefix="09")
    psh.save()
    
    psh = ParshaName(book_name=devarim, name='Haazinu', display='Parshat Haazinu',seq_number=52, prefix="10")
    psh.save()
    
    psh = ParshaName(book_name=devarim, name="V'ZotHaBerachah",display="Parshat V'Zot HaBerachah",seq_number=53, prefix="11")
    psh.save()
            


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(
        """
        Program Text 2 Database is designed to receive the bucket structure
        as text input (either stdin or files) and will parse and add the 
        files and folders to the database.
        
        From another program or the python shell do:
        import text2db
        text2db.text2db('name_of_file.txt')
        """
        )
    
    parser.add_argument('--clear', help='if set will delete all objects from the MusicDirectory and the MusicFile tables.', action='store_true')
    
    parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    
    args = parser.parse_args()
    
    # If you would call fileinput.input() without files it would try to process all arguments.
    # We pass '-' as only file when there are no files which will cause fileinput to read from stdin
    build_db_from_text(fileinput.input(files=args.files if len(args.files) > 0 else ('-', )), args.clear)
    

