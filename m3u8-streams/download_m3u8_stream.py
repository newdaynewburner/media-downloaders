#!/usr/bin/python3

"""
download_m3u8_stream.py

Downloads stream as MP4
"""

import sys
import m3u8_To_MP4

# Begin execution
if __name__ == "__main__":
    for arg in sys.argv[1:]:
        m3u8_To_MP4.multithread_download(arg)
        
    print("Done!")
    exit(0)