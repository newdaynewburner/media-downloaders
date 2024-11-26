#!/usr/bin/python3

"""
add_genre_tag_by_artist.py

Automatically add the genre tag to all songs by
a given artist based on a SQLite DB of artists and
their associated genre
"""

import os
import sys
import sqlite3
import eyed3

def add_genre_tag_by_artist(argv):
    """ Add appropriate genre tag from DB, or if
    artist not in file, prompt for their genre and add 
    that info
    
    Arguments:
        argv - list - MP3s to append genre tag to
        
    Returns:
        None
    """
    
    database = "artist_genre_data.db"
    if os.path.exists(database) != True:
        db_con = sqlite3.connect(database)
        db_cur = db_con.cursor()
        db_cur.execute("CREATE TABLE artist_genre_data(artist, genre)")
        db_con.commit()
        
    else:
        db_con = sqlite3.connect(database)
        db_cur = db_con.cursor()
        
    for arg in argv:
        mp3_file = eyed3.load(arg)
        
        print("Current song:")
        print("\t{}".format(arg))
        print("")
        
        if mp3_file.tag.artist is None:
            print("Artist tag empty! Please specify one below:")
            artist_tag = input("Artist: ")
            mp3_file.tag.artist = artist_tag
            mp3_file.tag.save()
            
        sql_query = "SELECT genre FROM artist_genre_data WHERE artist='{}'".format(mp3_file.tag.artist)
        db_response = db_cur.execute(sql_query)
        result = db_response.fetchone()
        
        if result is None:
            print("The artist '{}' was not found in the database! Please provide".format(mp3_file.tag.artist))
            print("their most commonly associated genre below:")
            artist_genre = input("Artist's genre: ")
            
            sql_query = "INSERT INTO artist_genre_data VALUES ('{0}', '{1}')".format(mp3_file.tag.artist, artist_genre)
            db_cur.execute(sql_query)
            db_con.commit()
            
        else:
            artist_genre = result[0]
            
        mp3_file.tag.genre = artist_genre
        mp3_file.tag.save()
        
    return None

# Begin execution
if __name__ == "__main__":
    add_genre_tag_by_artist(sys.argv[1:])