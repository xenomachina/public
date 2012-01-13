#!/usr/bin/python
# coding=utf-8

import sys

from mutagen.id3 import ID3

"""
Extracts APIC image from ID3 tags and writes it to a file.

Usage: extract_apic.py INPUT_MP3 OUTPUT_JPG
"""

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

def dumpAPIC(in_fnam, out_fnam):
  id3 = ID3(in_fnam)
  apic = id3.get('APIC:')
  if apic is None:
    print "No APIC: in %r" % in_fnam
    return

  assert apic.encoding == 0
  assert apic.mime == u'image/jpeg'
  assert apic.type == 3
  open(out_fnam, 'wb').write(apic.data)

def main(argv):
  in_fnam, out_fnam = argv[1:]
  dumpAPIC(in_fnam, out_fnam)

if __name__ == '__main__':
  main(sys.argv)
