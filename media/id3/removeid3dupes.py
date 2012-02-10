#!/usr/bin/python

import sys
import types

from mutagen.id3 import ID3

"""
Removes duplicate ID3 tag frames.
"""

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

"""
Removes duplicate ID3 frames.

For some reason Grip (or one of the tools it calls out to) put a bunch
of duplicate ID3 frames in a bunch of my MP3s.
"""

def removeDuplicateId3Frames(fnam):
  print "Reading", fnam
  id3 = ID3(fnam)
  frame_dicts = []
  remove_indices = []
  index = 0
  for frame in id3.frames:
    frame_dict = FrameToDict(frame)
    if frame_dict in frame_dicts:
      remove_indices.append(index)
    else:
      frame_dicts.append(frame_dict)
    index += 1
  remove_indices.reverse()
  for index in remove_indices:
    print "Removing duplicate %s frame #%d" % (id3.frames[index].header.id, index)
    #id3.frames.removeFrameByIndex(index)  # HAS A BUG
    list.__delitem__(id3.frames, index) #so use this instead
  if remove_indices:
    id3.update()

def FrameToDict(frame):
  frame_dict = {'header.id': frame.header.id}
  for attrname in dir(frame):
    if not attrname.startswith('_'): 
      attrvalue = getattr(frame, attrname)
      if isinstance(attrvalue, eyeD3.frames.FrameHeader):
        attrvalue = attrvalue.render(0)
      if type(attrvalue) is not types.MethodType:
        frame_dict[attrname] = attrvalue
  return frame_dict

def main(argv):
  for fnam in argv[1:]:
    try:
      removeDuplicateId3Frames(fnam)
    except ValueError, e:
      print e.message
    except TypeError, e:
      print e.message

if __name__ == '__main__':
  main(sys.argv)
