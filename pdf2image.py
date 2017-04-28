# Convert a pdf file to 1 or more jpg images (1 image per page).
# Store in a directory? GZip file?

# import some libraries
import argparse

# import other libraries here
from wand.image import Image
import os
import tempfile
import re

import string
import random

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# Class and Function Definitions
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

def id_generator_secure(size=6, chars=string.ascii_uppercase + string.digits):
    """
        Retruns a random string of uppercase letters and digits in a secure manner 
        suitable for generating passwords and keys. random.SystemRandom() generates 
        cryptographically secure PRNGs.
    """
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
        Returns a random string of uppercase letters and digits.
    """
    return ''.join(random.choice(chars) for _ in range(size))


def pdf2image(full_path, save_folder, resolution=150, format='jpg', debug=False) :
    ''' 
        Converts the pdf_file in the path to a series of images, one for
        each pdf page.
    '''
    
    # if debug: print full_path, resolution, format
    if (debug):
        print('inside pdf2image...')
        print(full_path, save_folder)
        
    try:
        if (debug):
            print('starting try')
        
        if not os.path.isfile(full_path):
            if (debug):
                print('not a file, trying to fix...')
            full_path = os.path.join(save_folder, full_path)
            # full_path = "./tmp/" + full_path
            with open(full_path, 'wb') as f:
                f.save()
        
        if os.path.isfile(full_path):
            if (debug): print('processing...')
            f = "tmp_" + id_generator(size=8) + "." + format
            if (debug): print(f)
            with Image(filename=full_path, resolution=resolution) as img:
                img.format=format
                img.save(filename=os.path.join(save_folder, f))
            the_images = get_images(full_path, save_folder, f, debug)
            trim_images(the_images[1])
            return the_images
    except IOError:
        if (debug): print('what?')
        raise
        
# done - pdf2iamge

def trim_images(image_list):
    for name in image_list:
        img = Image(filename=name)
        img.trim()
        img.save(filename=name)



def get_images(full_path, save_folder, result, debug=False):
    """
        Returns a tuple with the key eq to the name of the pdf file, and the value
        a sorted array of images that start with first 12 characters of result.
        result = a STRING representing names of the image files created.
        
        RETURNS: (key, [val1, val2])
    """
    if (debug): print(full_path, save_folder, result)
    g = re.compile(result[:12])
    images = list(filter(g.match, os.listdir(save_folder)))
    images.sort()
    if debug: print(images)
    
    base_name = os.path.basename(full_path)
    if debug: print(base_name)
    
    final = ( base_name, images )
    if debug: print(final)
    
    return final

# done - get_array_of_images


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------------------
# ----------------------------------------------------------------------

if __name__ == '__main__':
    
    # set up the command line arguments
    parser = argparse.ArgumentParser("""
    Example usage from within another python program or the python shell:
    import pdf2image
    import re
    import os
    result = pdf2image.pdf2image('file.pdf')
    g = re.compile(result[:12])
    array_of_images = filter(g.match, os.listdir('./tmp'))
    array_of_images.sort()
    !! At this point array_of_images is the images required, in order to display
    the original PDF as a series of images.!!
    """)
    
    parser.add_argument("full_path", help="include the full path to the pdf document to convert")
    
    parser.add_argument("--debug", help="set for additional print outs of information while the program runs", action="store_true")
    
    parser.add_argument("--resolution", type=int, help="the resolution to save the images as", default=150)

    parser.add_argument("--format", type=str, choices=['jpg', 'png'], help="format to create the images in - jpg or png", default='jpg')    

    args = parser.parse_args()
    
    pdf2image(full_path=args.full_path, save_folder=".",resolution=args.resolution, format=args.format, debug=args.debug)


# TO DO:
# For each PDF file, add the meta data below to the AWS file properties
# Content-Type: application/pdf
# Content-Disposition: attachment
