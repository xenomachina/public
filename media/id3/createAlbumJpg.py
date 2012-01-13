#!/usr/bin/python
# coding=utf-8

import os
import sys

import extract_apic

"""
Generates "album.jpg" file for each corresonding music file.

Usage:
  createAlbumJpg.py INPUT_MP3S...

Example:
  find Music/albums/ -name '*.mp3' -print0 | xargs -0 createAlbumJpg.py
"""

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

def main(argv):
  for fnam in argv[1:]:
    album_fnam = os.path.join(os.path.dirname(fnam), "album.jpg")
    if os.path.exists(album_fnam):
      print '%r already exists.' % album_fnam
    else:
      extract_apic.dumpAPIC(fnam, album_fnam)

if __name__ == '__main__':
  main(sys.argv)
