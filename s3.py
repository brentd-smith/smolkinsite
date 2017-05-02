import zipfile
import os
import os.path
import pdf2image
import glob
import shutil
import boto3 # S3
from text2torah import get_object_key
import argparse

NAME_OF_BUCKET = None
try:
    NAME_OF_BUCKET = os.environ['BUCKET_NAME']
except KeyError:
    NAME_OF_BUCKET = "testing-file-uploads"
    
## Connect to a bucket
s3 = boto3.resource('s3')

"""
Given a ZIP Archive file
1. Connect to S3 storage
2. For each file in the ZIP Archive, upload to S3 with the correct object key
?? Set security/user settings as appropriate ??
"""

def upload_zip(zip_file_name, debug=False):

    if (debug): print("Bucket Name = {}".format(NAME_OF_BUCKET))

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
                if (debug): print("\tStoring {} into S3 Bucket {}".format(final_key, NAME_OF_BUCKET))
                try:
                    s3.Bucket(NAME_OF_BUCKET).put_object(Key=final_key, Body=myfile.read(), ACL='public-read')
                except Exception, e:
                    raise e

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
    
    # pdf2image(full_path=args.full_path, save_folder=".",resolution=args.resolution, format=args.format, debug=args.debug)
    upload_zip(zip_file_name=args.zip_file_name, debug=args.debug)
