#!/usr/bin/python3

"""
album_downloader.py

Download MP3 format albums from YouTube playlists
"""

import os
import sys
import subprocess
import eyed3
from pytubefix import YouTube, Playlist

# CONFIGURATION
# You can tweak the values here to alter the
# scripts settings and change how it works :)
config = {
    "automatically_create_album_dir": True,
}

def album_downloader(config, argv):
    """ Download all videos in a playlist, convert to MP3, and 
    add tags and format as a music album
    
    Arguments:
        config - dict - Script configuration settings
        argv - list - List of user supplied YT playlist URLs
        
    Returns:
        None
    """
    
    for arg in argv:
        pl = Playlist(arg)
        print("Beginning download of album:")
        print(pl.title)
        print("")
        
        if config["automatically_create_album_dir"] == False:
            print("Please choose a name for the new albums directory:")
            album_dir = input("[Album directory]: ")
            print("")
        else:
            album_dir = pl.title
        
        os.mkdir(album_dir)
        os.chdir(album_dir)
                
        print("Please provide album tag info:")
        album_id3_tags = {}
        album_id3_tags["album_name"] = input("[Album name]: ")
        album_id3_tags["artist"] = input("[Artist]: ")
        album_id3_tags["genre"] = input("[Genre]: ")
        album_id3_tags["year"] = input("[Release year]: ")
        print("")
        
        video_urls = pl.urls
        track_num = 1
        for video_url in video_urls:
            yt = YouTube(video_url)
            print("Starting download of song:")
            print(yt.title)
            print("")
            print("Please provide song-specific tag info:")
            song_id3_tags = {}
            
            song_id3_tags["track_num"] = track_num
            song_id3_tags["title"] = input("[Song title]: ")
            
            dl_filename = "{0}. {1}.mp3".format(song_id3_tags["track_num"], song_id3_tags["title"])
            
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
            mp3_file.tag.track_num = song_id3_tags["track_num"]
            mp3_file.tag.title = song_id3_tags["title"]
            mp3_file.tag.artist = album_id3_tags["artist"]
            mp3_file.tag.album = album_id3_tags["album_name"]
            mp3_file.tag.genre = album_id3_tags["genre"]
            mp3_file.tag.year = album_id3_tags["year"]
            mp3_file.tag.save()
            print("")
            
            track_num = track_num + 1
            
        print("Download complete!")
        print("Downloaded album: {}".format(album_dir))
        
    return None
        
        

# Begin execution
if __name__ == "__main__":
    album_downloader(config, sys.argv[1:])