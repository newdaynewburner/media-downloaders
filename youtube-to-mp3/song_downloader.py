#!/usr/bin/python3

"""
song_downloader.py

Download songs from YouTube videos
"""

import os
import sys
import subprocess
import eyed3
from pytubefix import YouTube

# CONFIGURATION
# You can tweak the values here to alter the
# scripts settings and change how it works :)
config = {
    "automatically_create_file_name": True,
}

def song_downloader(config, argv):
    """ Download audio from YT videos and convert
    to MP3 format
    
    Arguments:
        config - dict - Script configuration settings
        argv - list - YT video URLs passed by the user
        
    Returns:
        None
    """
    for arg in argv:
        yt = YouTube(arg)
        
        print("Beginning download of video:")
        print(yt.title)
        print("")
        
        if config["automatically_create_file_name"] == False:
            print("Please enter a filename for this download")
            dl_filename = input("[New filename]: ")
            print("")
        else:
            dl_filename = "{}.mp3".format(yt.title)
        
        print("Please provide MP3 tag info")
        id3_tags = {}
        id3_tags["title"] = input("[Song title]: ")
        id3_tags["artist"] = input("[Artist]: ")
        id3_tags["genre"] = input("[Genre]: ")
        print("")
        
        print("Downloading...")
        raw_audio = yt.streams.filter(only_audio=True).first()
        raw_audio_file = raw_audio.download()
        
        print("Converting...")
        convert_command = """ffmpeg -hide_banner -loglevel error -i "{0}" "{1}" """.format(raw_audio_file, dl_filename)
        subprocess.check_output(convert_command, shell=True)
        os.remove(raw_audio_file)
        
        print("Tagging...")
        mp3_file = eyed3.load(dl_filename)
        mp3_file.initTag()
        mp3_file.tag.title = id3_tags["title"]
        mp3_file.tag.artist = id3_tags["artist"]
        mp3_file.tag.genre = id3_tags["genre"]
        mp3_file.tag.save()
            
        print("Download complete!")
        print("Downloaded filename: {}".format(dl_filename))
        
    return None
               
# Begin execution
if __name__ == "__main__":
    song_downloader(config, sys.argv[1:])