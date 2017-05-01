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
    name_of_bucket = "testing-file-uploads"
    
## Connect to a bucket
s3 = boto3.resource('s3')

"""
Given a ZIP Archive file
1. Connect to S3 storage
2. For each file in the ZIP Archive, upload to S3 with the correct object key
?? Set security/user settings as appropriate ??
"""

def upload_zip(zip_file_name, debug=False):
    
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
    
    # Copy all files to the S3 bucket
    with zipfile.ZipFile(zip_file_name) as zf:
        for info in zf.infolist():
            with zf.open(info.filename) as myfile:
                # 07 - Torah Readings/03 - Vayikra (Leviticus)/09.5 Parshat Behar - Bechukotai
                final_key = os.path.normpath(os.path.join(the_key, info.filename))
                if (debug): print("\tStoring {} into S3 Bucket {}".format(final_key, name_of_bucket))
                s3.Bucket(name_of_bucket).put_object(Key=final_key, Body=myfile.read(), ACL='public-read')
            
# works even when the "folders" my, key, and name have not been created yet
# s3.Object(name_of_bucket, "my/key/name/services.txt").upload_file("services.txt")

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
