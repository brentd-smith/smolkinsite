import zipfile
import os
import os.path
import pdf2image
import glob
import shutil
import boto3 # S3
from text2torah import get_object_key
import argparse
import logging
import logging.handlers

class SongsRepository:
    """Interact with the repository of songs."""

    # Filename where downloaded list will be stored, versions
    # handled by the RotatingFileHandler via the logging system.
    LOG_FILENAME = 'torah_readings.txt'
  
    def __init__(self):
        try:
            self.NAME_OF_BUCKET = os.environ['BUCKET_NAME']
        except KeyError:
            self.NAME_OF_BUCKET = "testing-file-uploads"
        self.s3 = boto3.resource('s3')

        self.repositoryLogger = logging.getLogger('SongsRepository')
        self.repositoryLogger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(message)s')
        self.handler = logging.handlers.RotatingFileHandler(
            self.LOG_FILENAME, maxBytes=4*1024, backupCount=5, )
        self.handler.setFormatter(formatter)
        self.repositoryLogger.addHandler(self.handler)


    def download_list(self, service_type):
        """
        Download a list of [service_type], either TorahReading or HaftarahReading.
        Create and/or update the torah_readings.txt file or the haftarah_readings.txt file.
        """
        if service_type == 'TorahReading':
            self.handler.doRollover()
            # download the current list of torah readings
            for obj in self.s3.Bucket(self.NAME_OF_BUCKET).objects.all():
                if obj.key.startswith('07 - Torah Readings/'):
                    self.repositoryLogger.info("{}".format(obj.key))
        elif service_type == 'HaftarahReading':
            # download the current list of haftarah readings
            pass

    def upload_one_file(self, file_name):
        """
        Upload a single file that has been updated.
        """
        pass

    def upload_zip(self, zip_file_name, debug=False):
        """
        Given a ZIP Archive file
        1. Connect to S3 storage
        2. For each file in the ZIP Archive, upload to S3 with the correct object key
        """
    
        if (debug): print("Bucket Name = {}".format(self.NAME_OF_BUCKET))
    
        # Get the PDF filename
        pdf_filename = ''
        if (debug): 
            print("Method: s3.upload_zip()")
            print("ZIP Archive: {}".format(zip_file_name))
            
        with zipfile.ZipFile(zip_file_name) as zf:
            for info in zf.infolist():
                filename, extension = os.path.splitext(info.filename)
                if (extension.upper() == '.PDF'):
                    pdf_filename = info.filename    
        
        # Extract the KEY information
        the_key = get_object_key(pdf_filename, debug)
        if (debug): print("Retrieved object key = {}".format(the_key))
        
        # Copy all files to the S3 bucket
        with zipfile.ZipFile(zip_file_name) as zf:
            if (debug): print("\tBeginning copy of all files to the S3 bucket...")
            for info in zf.infolist():
                if (debug): print("\tInside for loop, info.filename = {}".format(info.filename))
                with zf.open(info.filename) as myfile:
                    if (debug): print("\tOpening file, ready to copy...")
                    # 07 - Torah Readings/03 - Vayikra (Leviticus)/09.5 Parshat Behar - Bechukotai
                    final_key = os.path.normpath(os.path.join(the_key, info.filename))
                    if (debug): print("\tStoring {} into S3 Bucket {}".format(final_key, self.NAME_OF_BUCKET))
                    try:
                        self.s3.Bucket(self.NAME_OF_BUCKET).put_object(Key=final_key, Body=myfile.read(), ACL='public-read')
                    except Exception:
                        import sys, traceback
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        # print the traceback
                        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                        # print the exception
                        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
                    else:
                        if (debug): print("\tCopying of data to S3 completed successfully.")
            
# works even when the "folders" my, key, and name have not been created yet
# s3.Object(NAME_OF_BUCKET, "my/key/name/services.txt").upload_file("services.txt")

# TODO: Security, ACL, need to set all uploads to public read...

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

if __name__ == '__main__':
    
    # set up the command line arguments
    parser = argparse.ArgumentParser("""
    Usage:
        
    """)
    
    parser.add_argument("zip_file_name", help="ZIP Archive file to process.")
    
    parser.add_argument("--debug", help="Set for additional print outs of information while the program runs", action="store_true")
    
    # parser.add_argument("--resolution", type=int, help="the resolution to save the images as", default=150)
    # parser.add_argument("--format", type=str, choices=['jpg', 'png'], help="format to create the images in - jpg or png", default='jpg')    

    args = parser.parse_args()
    
    repository = SongsRepository()
    # pdf2image(full_path=args.full_path, save_folder=".",resolution=args.resolution, format=args.format, debug=args.debug)
    repository.load_zip(zip_file_name=args.zip_file_name, debug=args.debug)
