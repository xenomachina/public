#!/usr/bin/python
# coding=utf-8

import sys

from mutagen.id3 import ID3

"""
Prints ID3 tags to stdout.
"""

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

def printId3(fnam):
  id3 = ID3(fnam)
  dirty = []
  for key in sorted(id3.keys()):
    value = id3[key]
    print '%s:' % key,
    if hasattr(value, 'encoding') and hasattr(value, 'text'):
      texts = value.text
      if type(texts) is unicode:
        texts = [texts]
      print ('\n' + ' ' * (len(key) + 2)).join(map(unicode, texts)).encode('utf-8')
    else:
      print '<non-text>'

def main(argv):
  for fnam in argv[1:]:
    printId3(fnam)

if __name__ == '__main__':
  main(sys.argv)
