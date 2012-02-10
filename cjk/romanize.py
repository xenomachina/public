#!/usr/bin/python
# coding=utf-8

import sys

from cjk.hanziToPinyin import hanziToPinyin
from StringIO import StringIO

"""
Entry-point for generic romanization.

Currently this only handles Mandarin romanization (Hanyu Pinyin) and
some language-neutral romanizations (eg: a few graphical characters and
full-width ASCII), but the idea is that if I ever add additional
routines for other languages, this could delegate to those as well.
"""

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

# Fall-through mapping of non-Latin1 characters to Latin1 rough equivalents.
# This does not include true-romanizations.
_TO_LATIN1 = {
  u'™': u'[TM]',
  u'♥': u'<3',
  u'★': u'*',
  u'、': u',',
  u'—': u'-',
}
# fullwidth to ascii mapping
for i in range(0xff01, 0xff5f):
  _TO_LATIN1[unichr(i)] = unichr(i - 0xfee0)

def RemapChars(s, char_map):
  result = StringIO()
  for c in s:
    result.write(char_map.get(c, c))
  return result.getvalue()

def Romanize(s):
  result = hanziToPinyin(s, lambda w:w.capitalize())
  result = RemapChars(result, _TO_LATIN1)
  return result

def main(argv):
  for line in sys.stdin:
    line = line.decode('utf-8').rstrip()
    print Romanize(line).encode('utf-8')

if __name__ == '__main__':
  main(sys.argv)
