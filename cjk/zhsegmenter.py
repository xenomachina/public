#!/usr/bin/python
# coding=utf-8

"""
Easy to use Chinese segmenter.

Uses mmseg to do the real work. This is just some easy-to-use wrappers.
"""

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

import sys
import unicodedata
from StringIO import StringIO

import mmseg
mmseg.dict_load_defaults()

def Segment(s):
  """
  Given a unicode string performs Chinese segmentation.

  Result is a list of unicode strings, each being one "segment". Nte
  that the underlying segmented will ocasionally throw out bits of text
  (particularly punctuation). This wrapper will preserve these
  substrings by including them as distinct "segments".
  """
  assert type(s) is unicode
  s = s.encode('utf-8')
  tokens = mmseg.Algorithm(s)
  result = []
  pos = 0
  for token in tokens:
    if token.start > pos:
      result.append(s[pos:token.start].decode('utf-8'))
    result.append(token.text.decode('utf-8'))
    pos = token.end
  if pos < len(s):
    result.append(s[pos:].decode('utf-8'))
  return result

def _letterish(c):
  """
  Identifies the characters that should have an intervening space when
  joining segments. Currently returns true iff the Unicode category
  starts with 'L' or 'N' (ie: is one of the letter or number categories).
  """
  category = unicodedata.category(c)
  result = c and category and category[0] in 'LN'
  return result

def JoinSegments(segments, delimiter=u' '):
  """
  Given a sequence of segments (unicode strings) returns a unicode
  string consisting of the sgments joined together with delimiter inserted
  in the "appropriate" places. Typical usage is:

    JoinSegments(Segment(unicode_string_containing_chinese_text))

  This would be a useful thing to do before parsing a search query or
  romanizing a string.
  """
  assert type(delimiter) is unicode
  result = StringIO()
  tail = False
  for seg in segments:
    head = _letterish(seg[0])
    if head and tail:
      result.write(delimiter)
    tail = _letterish(seg[-1])
    result.write(seg)
  return result.getvalue()

def main(argv):
  """
  Simple interactive test harness. Enter a line of text and see how it's
  segmented and joined.
  """
  for line in sys.stdin:
    line = line.decode('utf-8').strip()
    print line.encode('utf-8')
    segments = Segment(line)
    for seg in segments:
      print '>>', (u'«' + seg + u'»').encode('utf-8')
    print '==', JoinSegments(segments).encode('utf-8')
    print

if __name__ == '__main__':
  main(sys.argv)
