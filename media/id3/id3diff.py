#!/usr/bin/python

import sys

from mutagen.id3 import ID3

"""
Compares ID3 tags of two diferent files.
"""

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

def id3diff(fnam1, fnam2):
  id3_1 = ID3(fnam1)
  id3_2 = ID3(fnam2)
  if id3_1 != id3_2:
    print fnam2
    keys = set(id3_1.keys())
    keys.update(id3_2.keys())
    for k in keys:
      if repr(id3_1.get(k)) != repr(id3_2.get(k)):
        print '\t%s' % k
        if len(repr(id3_1.get(k))) > 160:
          print '\t\t1: %d repr' % len(repr(id3_1.get(k)))
        else:
          print '\t\t1: %r' % id3_1.get(k)
        if len(repr(id3_2.get(k))) > 160:
          print '\t\t2: %d repr' % len(repr(id3_2.get(k)))
        else:
          print '\t\t2: %r' % id3_2.get(k)
    #print '\t%s' % (id3_2.keys())


def main(argv):
  before, after = argv[1:]
  id3diff(before, after)

if __name__ == '__main__':
  main(sys.argv)
