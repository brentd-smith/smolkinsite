import zipfile
import os
import os.path
import pdf2image
import glob
import shutil
import argparse
import text2torah
import sys, traceback
import logging

class ZipRepository:
    
    def __init__(self, serviceType='TorahReading'):
        self.repositoryLogger = logging.getLogger('ZipRepository')
        self.serviceType = serviceType

    def createImagesFromPdf(self, zip_file_name, debug=False):
        """
        Extract data from a zip file, split the PDF into multiple PNG image files 
        and crop whitespace.
        """
        to_append = []
        
        self.repositoryLogger.debug("Method: ZipRepository.createImagesFromPdf()")
        self.repositoryLogger.debug("ZIP Archive: {}".format(zip_file_name))
            
        with zipfile.ZipFile(zip_file_name) as zf:
            
            for info in zf.infolist():
        
                self.repositoryLogger.debug(info.filename)
                filename, extension = os.path.splitext(info.filename)
        
                if (extension.upper() == '.PDF'):
                    try:
                        zf.extract(info.filename, path=".", pwd=None)
                        
                        # pdf2image returns a tuple like this:
                        # ('2nd Triennial Breshit 5th Aliyah.pdf', ['tmp_ON6PPGIU-0.png', 'tmp_ON6PPGIU-1.png', 'tmp_ON6PPGIU-2.png'])
                        the_images = pdf2image.pdf2image(info.filename, ".", 300, format="png", debug=False)
                        for f in the_images[1]:
                            tmp = f[:12]
                            new_name = f.replace(tmp, filename, 1)
                            self.repositoryLogger.debug("Changing name from {} to {}".format(f, new_name))
                            shutil.move(f, new_name)
                            to_append.append(new_name)
                        
                        # clean up, remove the PDF file from the file system
                        os.remove(info.filename)
                    except KeyError:
                        print('ERROR: Did not find {} in zip file'.format(info.filename))
                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
                        self.repositoryLogger.critical("Problem when trying to extract images from pdf named {}".format(zip_file_name))
                    else:
                        self.repositoryLogger.debug("Successfully extracted and cropped image files...")
                        
        
        # add the new image files created from the PDF
        with zipfile.ZipFile(zip_file_name, mode='a') as zf:
            try:
                for f in to_append:
                    self.repositoryLogger.debug("Added file {} to the archive.".format(f))
                    zf.write(f)
                    self.repositoryLogger.debug("Removing file: {}".format(f))
                    os.remove(f)
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
                traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
                self.repositoryLogger.critical("Problem when trying to add image files into the archive {}".format(zip_file_name))
            else:
                self.repositoryLogger.debug("Successfully added new image file names...")
        
        # show the contents of the final ZIP Archive after processing
        self.repositoryLogger.debug("Final results of processing....")
        self.repositoryLogger.debug("ZIP Archive: {}".format(zip_file_name))
        with zipfile.ZipFile(zip_file_name, mode='r') as zf:
            for info in zf.infolist():
                self.repositoryLogger.debug(info.filename)
    
    def loadMetadataToDb(self, zip_file_name, debug=False):
        
        # Get the PDF filename
        pdf_filename = ''
        self.repositoryLogger.debug("Method: zipTorah.loadMetadataToDb()")
        self.repositoryLogger.debug("ZIP Archive: {}".format(zip_file_name))
            
        with zipfile.ZipFile(zip_file_name) as zf:
            for info in zf.infolist():
                filename, extension = os.path.splitext(info.filename)
                if (extension.upper() == '.PDF'):
                    pdf_filename = info.filename    
        
        # Extract the KEY information
        # Will be in format like: "07 - Torah Readings/01 - Breshit (Genesis)/02 Parshat Noach/3rd Triennial Noach 6th Aliyah"
        the_key = text2torah.get_object_key(pdf_filename, debug)
        
        key_list = []
        with zipfile.ZipFile(zip_file_name) as zf:
            for info in zf.infolist():
                key_list.append(os.path.normpath(os.path.join(the_key, info.filename)))
        
        # TODO: Delete equivalent torah readings from db first prior to insert
        # TorahReading.objects.filter(parsha='Behar-Bechukotai').filter(triennial='1st').filter(aliyah='6th')
        
        # Add the meta data to the database
        for k in key_list:
            self.repositoryLogger.debug("Processing one line of meta data = {}".format(k))
            text2torah.process_one_line(k, 0, False)

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
    createImagesFromPdf(zip_file_name=args.zip_file_name, debug=args.debug)
