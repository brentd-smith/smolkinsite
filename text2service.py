import argparse
import fileinput
import re
import sys
from songs.models import ServiceName, Song

PARSERS = { 
    'dir': r"^(\d+.?\d*)?\s?[A|B]?\s?-?\s?([a-zA-Z_\s\W\d]+)",    # directory name and sort order
}

ROOTS = set()
DIRECTORIES = set()

valid_dir_name = re.compile(PARSERS['dir'])

def process_one_line(line, count, debug=False):

    line = line.rstrip("\n\r")
    line = line.rstrip('/')
    folders = line.split('/')
    if len(folders) == 3:
        if (debug): print('folders=', folders)
        service_folder = folders[0]
        # if service_folder.find("Kabbalat Shabbat") >= 0:
        service_name = valid_dir_name.match(service_folder).group(2)
        if (debug): print('ServiceName=', service_name)
        service_key = service_name.replace(" ", "")
        srv = ServiceName.objects.get(pk=service_key)
        if (debug): print('srv.name=', srv.name)
        
        song_folder = folders[1]
        if (debug): print('SongFolder=', song_folder)
        
        song_name = valid_dir_name.match(song_folder).group(2)
        if (debug): print('SongName=', song_name)
        
        page_number = int(valid_dir_name.match(song_folder).group(1))
        if (debug): print('PageNumber=', page_number)
        
        file_folder = folders[2]
        file_name = valid_dir_name.match(file_folder).group(2)
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
        
        sg = Song(
            service_name=srv, 
            name=song_name.replace(" ", ""), 
            display=song_name, 
            s3_obj_key=line, 
            extension=ext, 
            page_number=page_number, 
            seq_number=page_number,
            file_name=file_name)
        sg.save()
        
        if (debug): print('sequence number = ', count)
# end process_one_line

def build_db_from_text(fh, clear=True):
    try:
        
        if clear:
            addServices()
            
        line_count = 0
        for line in fh:
            if line.find('/work/') < 0 :
                process_one_line(line, line_count)
            line_count += 1
            # if line_count > 500: break
        fh.close()
    except:
        # print line_count, line
        print("Something bad happened:", sys.exc_info()[0])
        fh.close()
        raise
# end build_db_from_text

def addServices():
    service_names = ServiceName.objects.all()
    service_names.delete()
    
    songs = Song.objects.all()
    songs.delete()

    sn = ServiceName("KabbalatShabbat", "Kabbalat Shabbat", 1)
    sn.save()
    
    sn = ServiceName("FridayNight", "Friday Night Maariv", 2)
    sn.save()
    
    sn = ServiceName("TorahService", "Shabbat Torah Service", 3)
    sn.save()
    
    sn = ServiceName("Musaf", "Shabbat Musaf Service", 4)
    sn.save()

def text2db(file_name='services.txt'):
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
    

