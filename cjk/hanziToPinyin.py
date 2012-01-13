#!/usr/bin/python
# coding=utf-8

"""
Mandarin Chinese to Hanyu Pinyin romanization.

This will segment chinese text, convert the characters to pinyin, and
also provides some options for delaing with tone marks.
"""

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

import codecs
import os
import pickle
import re
import sys

import cjk.zhsegmenter

import mmseg
mmseg.dict_load_defaults()

# An approximation of tone marks, in ISO Latin-1.  Second and fourth
# tones are easy, we use acute and grave accents.  Third tone we use
# circumflex, which is upside-down but not too bad.  First tone kind of
# sucks. It's supposed to be a horizontal bar, but notheing like that
# exist in Latin-1. Instead we use diaeresis (umlaut). Not too bad,
# except pinyin already uses ü, so a u with the first tone doesn't have
# an unambiguous representation.  Also, we can't put a tone mark on ü.
_LATIN1_TONE_MARKS = {
  (u'a', 1): u'ã',
  (u'a', 2): u'á',
  (u'a', 3): u'â',
  (u'a', 4): u'à',
  (u'a', 5): u'a',
  (u'e', 1): u'ë',
  (u'e', 2): u'é',
  (u'e', 3): u'ê',
  (u'e', 4): u'è',
  (u'e', 5): u'e',
  (u'i', 1): u'ï',
  (u'i', 2): u'í',
  (u'i', 3): u'î',
  (u'i', 4): u'ì',
  (u'i', 5): u'i',
  (u'o', 1): u'ö',
  (u'o', 2): u'ó',
  (u'o', 3): u'ô',
  (u'o', 4): u'ò',
  (u'o', 5): u'o',
  (u'u', 1): u'ü',
  (u'u', 2): u'ú',
  (u'u', 3): u'û',
  (u'u', 4): u'ù',
  (u'u', 5): u'u',
}
def Latin1ToneMarks(c, tone):
  return _LATIN1_TONE_MARKS[c, tone]

PINLU_REGEX = re.compile(ur'([\xfca-z]+[1-5])\(([0-9]+)\)')
def _pinlu_str_to_tuple(s):
  s = s.strip()
  pinyin, freq = PINLU_REGEX.match(s).groups()
  return freq, pinyin

TONE_NUMBER_REGEX = re.compile(ur'^([a-z\xfc]+)([12345])$')
def InlineToneMark(s, markFunc):
  """
  Given a string containing a numerical pinyin syllable, eg: "huai4",
  returns the equivalent string with the tone mark inlined.

  markFunc is a function that takes a single character (a pinyin vowel)
  and a tone number and returns the string representation of the
  character with the tone mark applied.
  """
  m = TONE_NUMBER_REGEX.match(s)
  if m:
    letters = m.group(1)
    tone = int(m.group(2))
    # this is based on http://www.romanization.com/pinyintonemarks/
    for vowel, offset in [
      (u'a', 0),
      (u'e', 0),
      (u'o', 0),
      (u'iu', 1),
      (u'ui', 1),
      (u'i', 0),
      (u'u', 0),
      (u'ü', 0)]:
      index = letters.find(vowel)
      if index >= 0:
        index += offset
        break
    assert index >= 0
    return (
        letters[:index]
        + markFunc(letters[index], tone)
        + letters[index + 1:])
  else:
    return s

def hanziToPinyin(s, f=lambda x:x):
  assert type(s) is unicode
  def repl(m):
    return InlineToneMark(_CHAR_TO_PINYIN[m.group(0)], Latin1ToneMarks)
  tokens = cjk.zhsegmenter.Segment(s)
  pinyins = []
  for token in tokens:
    pinyin = HANZI_CHAR_RE.sub(repl, token)
    if pinyin != token:
      pinyin = f(pinyin)
    pinyins.append(pinyin)
  return cjk.zhsegmenter.JoinSegments(pinyins)

_CHAR_TO_PINYIN = pickle.load(
    open(os.path.join(os.path.dirname(__file__), 'unihan/HanyuPinlu.pkl')))

for c, pinlus in _CHAR_TO_PINYIN.items():
    pinlus = [
        _pinlu_str_to_tuple(x.decode('utf-8').strip())
        for x in pinlus.split(',')]
    pinlus.sort()
    _CHAR_TO_PINYIN[c] = pinlus[-1][1]

_CHAR_TO_MANDARIN = pickle.load(
    open(os.path.join(os.path.dirname(__file__), 'unihan/Mandarin.pkl')))
for c, pinyin in _CHAR_TO_MANDARIN.items():
  pinyin = pinyin.lower().split()[0].decode('utf-8')
  #if c in _CHAR_TO_PINYIN:
  #  if _CHAR_TO_PINYIN[c] != pinyin:
  #    print 'Warning: %r != %r' % (_CHAR_TO_PINYIN[c], pinyin)
  _CHAR_TO_PINYIN[c] = pinyin
del _CHAR_TO_MANDARIN

HANZI_CHAR_RE = re.compile('[' + re.escape(''.join(_CHAR_TO_PINYIN.keys())) + ']')

assert u'\u796d' in _CHAR_TO_PINYIN

if __name__ == '__main__':
  print "ready."
  for line in sys.stdin:
    line = line.strip().decode('utf-8')
    line = hanziToPinyin(line)
    assert line.encode('latin1').decode('latin1') == line
    print line.encode('utf-8')
