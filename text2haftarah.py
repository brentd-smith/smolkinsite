import argparse
import fileinput
import re
import sys
from music.models import BookName, ParshaName, HaftarahReading

# '1st Triennial Ki Tisa 2nd Aliyah'
PARSERS = { 
    'dir': r"^(\d+.?\d*)?\s?[A|B]?\s?-?\s?([a-zA-Z_\s\W\d]+)",                      # directory name and sort order
    'parsha': r"^\d{2}.?\d?\sParshat\s(.+)$",                                       # parsha name
}

ROOTS = set()
DIRECTORIES = set()

valid_dir_name = re.compile(PARSERS['dir'])
valid_parsha_name = re.compile(PARSERS['parsha'])

# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Haftarah for Ki Tetzei - Hebrew-0.jpg
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Haftarah for Ki Tetzei - Hebrew-1.jpg
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Haftarah for Ki Tetzei - Hebrew.pdf
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Haftarah for Ki Tetzei.mp3
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Isa 54-1.mp3
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Isa 54-10.mp3
# 08 - Haftarah Readings/05 - Devarim (Deuteronomy)/06 Parshat Ki Tetzei/Isa 54-2.mp3
def process_one_line(line, count):

    line = line.rstrip("\n\r")
    line = line.rstrip('/')
    folders = line.split('/')
    if len(folders) == 4:
        print 's3_obj_key=', line
        print 'folders=', folders
        
        book_folder = folders[1]
        print 'BookFolder=', book_folder
        
        bs = book_folder.split(' ')
        book_name = bs[2]
        print 'BookName=', book_name
        bk = BookName.objects.get(pk=book_name)
        
        parsha_folder = folders[2]
        parsha_name = valid_parsha_name.match(parsha_folder).group(1)
        parsha_name = parsha_name.replace(" ", "")
        print 'ParshaName=', parsha_name
        psh = ParshaName.objects.get(pk=parsha_name)

        file_name = folders[3]
        print 'FileName=',file_name
        
        # Figure out the extension
        ext=''
        if file_name.lower().endswith(".mp3") :
            ext = "mp3"
        elif file_name.lower().endswith(".pdf") :
            ext = "pdf"
        elif file_name.lower().endswith(".jpg") :
            ext = "jpg"
        print 'Extension=',ext
        
    
        htr = HaftarahReading(
            parsha=psh,
            extension=ext,
            s3_obj_key=line,
            seq_number=count,
            file_name=file_name
            )
        htr.save()
        

        print 'sequence number = ', count
# end process_one_line

def build_db_from_text(fh, clear=True):
    try:
        
        if clear:
            haftaras = HaftarahReading.objects.all()
            haftaras.delete()
            
            # book_names = BookName.objects.all()
            # book_names.delete()

            # parshas = ParshaName.objects.all()
            # parshas.delete()

            # torah = TorahReading.objects.all()
            # torah.delete()

            # # add books            
            # breshit = BookName(name='Breshit', display='Breshit (Genesis)', seq_number=1)
            # breshit.save()
            
            # shemot = BookName("Shemot", "Shemot (Exodus)", 2)
            # shemot.save()

            # vayikra = BookName("Vayikra", "Vayikra (Leviticus)", 3)
            # vayikra.save()

            # bemidbar = BookName("Bemidbar", "Bemidbar (Numbers)", 4)
            # bemidbar.save()

            # devarim = BookName("Devarim", "Devarim (Deuteronomy)", 5)
            # devarim.save()
            
            # breshit = BookName.objects.get(pk='Breshit')
            # print breshit.name
            # shemot = BookName.objects.get(pk='Shemot')
            # print shemot.name
            # vayikra = BookName.objects.get(pk='Vayikra')
            # print vayikra.name
            # bemidbar = BookName.objects.get(pk='Bemidbar')
            # print bemidbar.name
            # devarim = BookName.objects.get(pk='Devarim')
            # print devarim.name
            
            # # add parshas
            # psh = ParshaName(book_name=breshit, name='Breshit', display='Parshat Breshit',seq_number=1)
            # psh.save()
            
            # # verify the foreign key is working as expected
            # tmp1 = ParshaName.objects.get(pk='Breshit')
            # print tmp1.name, tmp1.display
            # print tmp1.book_name.name
            
            # psh = ParshaName(book_name=breshit, name='Noach', display='Parshat Noach',seq_number=2)
            # psh.save()
            
            # psh = ParshaName(book_name=breshit, name='LechLecha', display='Parshat Lech Lecha',seq_number=3)
            # psh.save()
            
            # psh = ParshaName(book_name=breshit, name='Vayera', display='Parshat Vayera',seq_number=4)
            # psh.save()
            
            # psh = ParshaName(book_name=breshit, name='ChayeSarah', display='Parshat Chaye Sarah',seq_number=5)
            # psh.save()
            
            # psh = ParshaName(book_name=breshit, name='Toldot', display='Parshat Toldot',seq_number=6)
            # psh.save()
            
            # psh = ParshaName(book_name=breshit, name='Vayetze', display='Parshat Vayetze',seq_number=7)
            # psh.save()
            
            # psh = ParshaName(book_name=breshit, name='Vayishlach', display='Parshat Vayishlach',seq_number=8)
            # psh.save()
            
            # psh = ParshaName(book_name=breshit, name='Vayeshev', display='Parshat Vayeshev',seq_number=9)
            # psh.save()
            
            # psh = ParshaName(book_name=breshit, name='Mikeitz', display='Parshat Mikeitz',seq_number=10)
            # psh.save()
            
            # psh = ParshaName(book_name=breshit, name='Vayigash', display='Parshat Vayigash',seq_number=11)
            # psh.save()
            
            # psh = ParshaName(book_name=breshit, name='Vayechi', display='Parshat Vayechi',seq_number=12)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name='Shemot', display='Parshat Shemot',seq_number=13)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name="Va'eira",display="Parshat Va'eira",seq_number=14)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name='Bo', display='Parshat Bo',seq_number=15)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name='Beshalach', display='Parshat Beshalach',seq_number=16)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name='Yitro', display='Parshat Yitro',seq_number=17)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name='Mishpatim', display='Parshat Mishpatim',seq_number=18)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name='Trumah', display='Parshat Trumah',seq_number=19)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name="T'tzaveh",display="Parshat T'tzaveh",seq_number=20)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name='KiTisa', display='Parshat Ki Tisa',seq_number=21)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name='Vayakhel', display='Parshat Vayakhel',seq_number=22)
            # psh.save()
            
            # psh = ParshaName(book_name=shemot, name='Pekudei', display='Parshat Pekudei',seq_number=23)
            # psh.save()
            
            # psh = ParshaName(book_name=vayikra, name='Vayikra', display='Parshat Vayikra',seq_number=24)
            # psh.save()
            
            # psh = ParshaName(book_name=vayikra, name='Tzav', display='Parshat Tzav',seq_number=25)
            # psh.save()
            
            # psh = ParshaName(book_name=vayikra, name='Shemini', display='Parshat Shemini',seq_number=26)
            # psh.save()
            
            # psh = ParshaName(book_name=vayikra, name='Tazria-Metzora', display='Parshat Tazria-Metzora',seq_number=27)
            # psh.save()
            
            # psh = ParshaName(book_name=vayikra, name='Metzora', display='Parshat Metzora',seq_number=28)
            # psh.save()
            
            # psh = ParshaName(book_name=vayikra, name='AchareiMot-Kedoshim', display='Parshat Acharei Mot-Kedoshim',seq_number=29)
            # psh.save()
            
            # psh = ParshaName(book_name=vayikra, name='Emor', display='Parshat Emor',seq_number=30)
            # psh.save()
            
            # psh = ParshaName(book_name=vayikra, name='Behar', display='Parshat Behar',seq_number=31)
            # psh.save()
            
            # psh = ParshaName(book_name=vayikra, name='Behar-Bechukotai', display='Parshat Behar - Bechukotai',seq_number=32)
            # psh.save()
            
            # psh = ParshaName(book_name=vayikra, name='Bechukotai', display='Parshat Bechukotai',seq_number=33)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='Bemidbar', display='Parshat Bemidbar',seq_number=34)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='Naso', display='Parshat Naso',seq_number=35)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='Behaalotcha', display='Parshat Behaalotcha',seq_number=36)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='Shelach', display='Parshat Shelach',seq_number=37)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='ShlachLecha', display='Parshat Shlach Lecha', seq_number=37)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='Korach', display='Parshat Korach',seq_number=38)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='Chukat', display='Parshat Chukat',seq_number=39)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='Balak', display='Parshat Balak',seq_number=40)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='Pinchas', display='Parshat Pinchas',seq_number=41)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='Matot', display='Parshat Matot',seq_number=42)
            # psh.save()
            
            # psh = ParshaName(book_name=bemidbar, name='Massei', display='Parshat Massei',seq_number=43)
            # psh.save()
            
            # psh = ParshaName(book_name=devarim, name='Devarim', display='Parshat Devarim',seq_number=44)
            # psh.save()
            
            # psh = ParshaName(book_name=devarim, name='Eikev', display='Parshat Eikev',seq_number=45)
            # psh.save()
            
            # psh = ParshaName(book_name=devarim, name="R'eh",display="Parshat R'eh",seq_number=46)
            # psh.save()
            
            # psh = ParshaName(book_name=devarim, name='Shoftim', display='Parshat Shoftim',seq_number=47)
            # psh.save()
            
            # psh = ParshaName(book_name=devarim, name='KiTetze', display='Parshat Ki Tetze',seq_number=48)
            # psh.save()
            
            # psh = ParshaName(book_name=devarim, name='KiTavo', display='Parshat Ki Tavo',seq_number=49)
            # psh.save()
            
            # psh = ParshaName(book_name=devarim, name='NitzavimVayelech', display='Parshat Nitzavim Vayelech',seq_number=50)
            # psh.save()
            
            # psh = ParshaName(book_name=devarim, name='Vayelech', display='Parshat Vayelech',seq_number=51)
            # psh.save()
            
            # psh = ParshaName(book_name=devarim, name='Haazinu', display='Parshat Haazinu',seq_number=52)
            # psh.save()
            
            # psh = ParshaName(book_name=devarim, name="V'ZotHaBerachah",display="Parshat V'Zot HaBerachah",seq_number=53)
            # psh.save()
            


        line_count = 0
        for line in fh:
            process_one_line(line, line_count)
            line_count += 1
        fh.close()
    except:
        # print line_count, line
        print "Something bad happened:", sys.exc_info()[0]
        fh.close()
        raise
# end build_db_from_text

def text2db(file_name='haftarah_readings.txt'):
    build_db_from_text(fileinput.input(file_name))
# end text2db

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
    

