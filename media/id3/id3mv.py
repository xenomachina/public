#!/usr/bin/python
# coding=utf-8

import sys
import os

import formatid3
import commands

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

def raiseError(error):
  raise error

def findFiles(top):
  if os.path.isfile(top):
    yield top
  else:
    for (dirpath, dirnames, filenames) in os.walk(
        top, onerror=raiseError, followlinks=True):
      for filename in filenames:
        yield os.path.join(dirpath, filename)

def computeDests(format, top):
  dests = set()
  for fnam in findFiles(top):
    if fnam.lower().endswith('.mp3'):
      dests.add(formatid3.formatId3(format, fnam))
  return dests

def id3mv(format, top):
  dests = computeDests(format, top)
  if len(dests) != 1:
    print >>sys.stderr, '%d destinations for %r:' % (len(dests), top)
    dests = sorted(dests)
    for dest in dests:
      print >>sys.stderr, '  %s' % unicode(dest).encode('utf-8')
  else:
    dest = dests.pop()
    if dest is None:
      print >>sys.stderr, 'No real destination for %r:' % top
    else:
      dest = dest.encode('utf-8')
      if dest == top:
        print >>sys.stderr, '%r not moving' % top
      else:
        print 'mv -iv' + commands.mkarg(top) + commands.mkarg(dest)

def main(argv):
  format = tuple(formatid3.parseFormat(argv[1].decode('utf-8')))
  #for fnam in argv[2:]:
  #  print formatid3.formatId3(format, fnam).encode('utf-8')
  for arg in argv[2:]:
    id3mv(format, arg)

if __name__ == '__main__':
  main(sys.argv)
