#!/usr/bin/python

import eyeD3
import re
import sys

"""
Repairs ID3 tags that were incorrectly marked as latin1 when they were
actually UTF-8.

I had a bunch of MP3s that I'd ripped/encoded with Grip. I don't know if
Grip or one of the many tools it calls out to was responsible, but the
encoding marker was set incorrectly.
"""

GETTER_RE = re.compile('^get([A-Z].*)$')

def reencodeValue(s):
  try:
    return s.encode('latin1').decode('utf-8')
  except UnicodeEncodeError:
    return s
  except UnicodeDecodeError:
    return s

def reencodeId3Tags(fnam):
  print "Reading", fnam
  tag = eyeD3.Tag()
  tag.link(fnam)
  print 'Old Album:', repr(tag.getAlbum())
  print 'Old Title:', repr(tag.getTitle())
  attrs = dir(tag)
  dirty = False
  for attr in attrs:
    m = GETTER_RE.match(attr)
    if m:
      prop_name = m.group(1)
      setter = ('set' + prop_name)
      if setter in attrs:
        prop_value = getattr(tag, attr)()
        if type(prop_value) is unicode:
          reencoded_value = reencodeValue(prop_value)
          if reencoded_value != prop_value:
            print '  re-encoding', prop_name, 'as', repr(reencoded_value)
            getattr(tag, setter)(reencoded_value)
            dirty = True
  if dirty:
    for frame in tag.frames:
      if isinstance(frame, eyeD3.frames.TextFrame):
        if frame.text and type(frame.text) is not unicode:
          raise "WTF!? " + repr(frame.text)
        frame.encoding = eyeD3.frames.UTF_8_ENCODING

    print '  saving updates to', fnam
    tag.update()
    tag = eyeD3.Tag()
    tag.link(fnam)
    print 'New Album:', repr(tag.getAlbum())
    print 'New Title:', repr(tag.getTitle())

def main(argv):
  for fnam in argv[1:]:
    reencodeId3Tags(fnam)

if __name__ == '__main__':
  main(sys.argv)
