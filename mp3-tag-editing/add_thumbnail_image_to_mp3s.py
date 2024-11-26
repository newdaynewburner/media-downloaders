#!/usr/bin/python3

"""
add_thumbnail_image_to_mp3s.py

Insert a thumbnail image
"""

import os
import sys
import eyed3

def add_thumbnail_image_to_mp3s(argv):
    """ Add a thumbnail image to MP3 files
    
    Arguments:
        argv - list - MP3 files to append image to
        
    Returns:
        None
    """
    
    print("Please specify image file to add:")
    thumbnail_image = input("[Image file]: ")
    
    for arg in argv:
        mp3_file = eyed3.load(arg)
        mp3_file.initTag(version=(2, 3, 0))
        with open(thumbnail_image, "rb") as image_file:
            image_data = image_file.read()
            
        mp3_file.tag.images.set(3, image_data, "image/jpeg", u"cover")
        mp3_file.tag.save()

# Begin execution
if __name__ == "__main__":
    add_thumbnail_image_to_mp3s(sys.argv[1:])