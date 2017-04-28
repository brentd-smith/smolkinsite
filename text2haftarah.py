import argparse
import fileinput
import re
import sys
from songs.models import BookName, ParshaName, HaftarahReading

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
def process_one_line(line, count, debug=False):

    line = line.rstrip("\n\r")
    line = line.rstrip('/')
    folders = line.split('/')
    if len(folders) == 4:
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
        parsha_name = valid_parsha_name.match(parsha_folder).group(1)
        parsha_name = parsha_name.replace(" ", "")
        if (debug): print('ParshaName=', parsha_name)
        psh = ParshaName.objects.get(pk=parsha_name)

        file_name = folders[3]
        if (debug): print('FileName=',file_name)
        
        # Figure out the extension
        ext=''
        if file_name.lower().endswith(".mp3") :
            ext = "mp3"
        elif file_name.lower().endswith(".pdf") :
            ext = "pdf"
        elif file_name.lower().endswith(".jpg") :
            ext = "jpg"
        if (debug): print('Extension=',ext)
        
    
        htr = HaftarahReading(
            parsha=psh,
            extension=ext,
            s3_obj_key=line,
            seq_number=count,
            file_name=file_name
            )
        htr.save()
        

        if (debug): print('sequence number = ', count)
# end process_one_line

def build_db_from_text(fh, clear=True):
    try:
        
        if clear:
            haftaras = HaftarahReading.objects.all()
            haftaras.delete()

        line_count = 0
        for line in fh:
            process_one_line(line, line_count)
            line_count += 1
        fh.close()
    except:
        # print(line_count, line
        print("Something bad happened:", sys.exc_info()[0])
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
    

