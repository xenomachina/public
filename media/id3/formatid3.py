#!/usr/bin/python
# coding=utf-8

import sys
import re
from StringIO import StringIO

from mutagen.id3 import ID3, NumericTextFrame, NumericPartTextFrame
from mutagen.id3 import ID3NoHeaderError

"""
Prints out formatted string based on ID3 tags. Format strings are
similar to those used by Grip.

Usage:
  formatid3.py FORMATSTRING MUSIC_FILE...

Example:
  $ formatid3.py '%a - %d - %t - %n' foo.mp3
  Artist - Album - 01 - Track Name
"""

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

class FormatNode(object):
  def format(self, id3, munge):
    abstract

class LiteralFormatNode(object):
  def __init__(self, value):
    self.__value = value

  def format(self, id3, munge):
    return self.__value

class FieldFormatNode(object):
  def __init__(self, field, prefix):
    self.__field = field
    self.__prefix = prefix

  def format(self, id3, munge):
    if self.__prefix:
      fmt = u'%' + self.__prefix
    else:
      fmt = u'%'
    frame = id3[self.__field]
    if isinstance(frame, NumericTextFrame) or isinstance(frame, NumericPartTextFrame):
      fmt += 'd'
      value = +frame
    else:
      fmt += 's'
      value = frame.text[0]
    return munge(fmt % value)


OBLITERATE_RE = re.compile(ur"[\000-\037'?]")
# TODO: put space in TO_UNDERSCORE_RE
TO_UNDERSCORE_RE = re.compile(ur"[/]")
TO_UNDERSCORE_HYPHEN_RE = re.compile(ur"[:]")
def munge(s):
  """
  Based on ABCDE's mungefilename.
  """
  return TO_UNDERSCORE_HYPHEN_RE.sub('_-',
      TO_UNDERSCORE_RE.sub('_',
        OBLITERATE_RE.sub('', s)))

def formatId3(fmts, fnam, munge=munge):
  try:
    id3 = ID3(fnam)
  except ID3NoHeaderError:
    return None
  out = StringIO()
  for fmt in fmts:
    try:
      out.write(fmt.format(id3, munge))
    except KeyError:
      return None
  return out.getvalue()

FORMAT_RE = re.compile('%([0-9]*)(?:\(([^()]*)\)|([a-zA-Z%]))')
def parseFormat(formatString):
  result = []
  pos = 0
  while True:
    m = FORMAT_RE.search(formatString, pos)
    if m:
      if m.start() > pos:
        result.append(LiteralFormatNode(formatString[pos:m.start()]))
      field = m.group(3)
      # TODO: add a format for the input filename?
      if field == '%':
        result.append(LiteralFormatNode(field))
      else:
        if field is None:
          field = m.group(2)
        else:
          field = {
              # These format specifiers ar based on GRIP
              't': 'TRCK', # track number
              'n': 'TIT2', # track name
              'd': 'TALB', # album ("disc") name
              'G': 'TCON', # genre string
              'y': 'TDRC', # year
              'a': 'TPE1', # artist
            }[field]
        result.append(FieldFormatNode(field, m.group(1)))
      pos = m.end()
    else:
      result.append(LiteralFormatNode(formatString[pos:]))
      break
  return result

def main(argv):
  format = parseFormat(argv[1].decode('utf-8'))
  for fnam in argv[2:]:
    print formatId3(format, fnam).encode('utf-8')

if __name__ == '__main__':
  main(sys.argv)
