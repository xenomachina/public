#!/usr/bin/python
# coding=utf-8

import sys
from StringIO import StringIO

import mutagen.id3
from mutagen.id3 import ID3
from mutagen.id3 import ID3NoHeaderError
from cjk.romanize import Romanize

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

def reencode(s):
  if type(s) is unicode:
    try:
      s = s.encode('latin1').decode('utf-8')
    except UnicodeEncodeError:
      pass
    except UnicodeDecodeError:
      pass
    assert type(s) is unicode
  return s

ROMANIZE_V2 = 1

def reencodeId3Tags(fnam):
  print "Reading", fnam
  try:
    id3 = ID3(fnam)
  except ID3NoHeaderError:
    print 'Skipping %s, no ID3' % fnam
    return
  #print 'Old Album:', repr(id3.get('TIT2'))
  #print 'Old Title:', repr(id3.get('TALB'))
  dirty = []
  v1=1
  for key in id3.keys():
    value = id3[key]
    romanize = mutagen.id3.Romanize
    if hasattr(value, 'encoding') and hasattr(value, 'text'):
      if value.encoding == 0:
        if type(value.text) is unicode:
          reencoded_text = reencode(value.text)
        else:
          assert type(value.text) is list
          reencoded_text = [reencode(t) for t in value.text]
        if reencoded_text != value.text:
          #print '  re-encoding', key, 'as', repr(reencoded_text)
          #print '  from', repr(value.text)
          value.encoding = 3
          value.text = reencoded_text
          dirty.append('broken encoding in %r' % key)
      if type(value.text) is unicode:
        romanized_text = Romanize(value.text)
      else:
        assert type(value.text) is list
        romanized_text = [Romanize(t) if type(t) is unicode else t for t in value.text]
      if romanized_text != value.text:
        if ROMANIZE_V2:
          value.text = romanized_text
          dirty.append('romanizing tags')
        else:
          romanize = lambda s: Romanize(s).encode('latin1')
          dirty.append('non-latin text -- adding romanized v1 tags')
          v1=2
  dirty.extend(id3.dirty)
  if dirty:
    print '  saving updates to %r: %s' % (fnam, ', '.join(dirty))
    # TODO: this depends on a patch to Mutagen that I have yet to submit.
    id3.save(v1=v1, romanize=romanize)
    #print 'New Album:', repr(id3.get('TIT2'))
    #print 'New Title:', repr(id3.get('TALB'))
  else:
    print '  no updates to', fnam

def main(argv):
  for fnam in argv[1:]:
    reencodeId3Tags(fnam)

if __name__ == '__main__':
  main(sys.argv)
