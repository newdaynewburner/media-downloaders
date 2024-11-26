#!/usr/n/python3

"""
normalize_misc_songs.py

For all songs passed in arguments, prompt user for correct title
and artist tags, wipe old tags and replace with new ones, and rename
the songs file in 'ARTIST - TITLE.mp3' convention
"""

import os
import sys
import eyed3

def normalize_misc_songs(argv):
    """ Prompt for correct tags, replace them, then
    rename the file
    
    Arguments:
        argv - list - MP3 files to normalize
        
    Returns:
        None
    """
    
    for arg in argv:
        mp3_file = eyed3.load(arg)
        if mp3_file.tag.title is not None:
            existing_title_tag = mp3_file.tag.title
        else:
            existing_title_tag = ""
            
        if mp3_file.tag.artist is not None:
            existing_artist_tag = mp3_file.tag.artist
        else:
            existing_artist_tag = ""
            
        #os.system("clear") # LINUX
        os.system("cls") # WINDOWS
        print("Current MP3 file:")
        print("\t{}".format(arg))
        print("Existing tags:")
        print("\tTitle: {0} | Artist: {1}".format(existing_title_tag, existing_artist_tag))
        print("")
        print("")
        print("Please enter the correct tag information below, or leave blank to keep:")
        new_title_tag = input("Title: ")
        if new_title_tag == "":
            new_title_tag = existing_title_tag
        new_artist_tag = input("Artist: ")
        if new_artist_tag == "":
            new_artist_tag = existing_artist_tag
            
        new_filename = "{0} - {1}.mp3".format(new_artist_tag, new_title_tag)
        
        mp3_file.tag.title = new_title_tag
        mp3_file.tag.artist = new_artist_tag
        mp3_file.tag.save()
        
        full_mp3_filepath = os.path.abspath(arg)
        directory, filename = os.path.split(full_mp3_filepath)
        full_new_filename = os.path.join(directory, new_filename)
        if os.path.exists(full_new_filename) != True:
            os.rename(full_mp3_filepath, full_new_filename)
        
    return None

# Begin execution
if __name__ == "__main__":
    normalize_misc_songs(sys.argv[1:])