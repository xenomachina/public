#!/usr/bin/python

import eyeD3
import sys
import types
from sets import Set

def removeDuplicateId3Frames(fnam):
  print "Reading", fnam
  tag = eyeD3.Tag()
  tag.link(fnam)
  frame_dicts = []
  remove_indices = []
  index = 0
  for frame in tag.frames:
    frame_dict = FrameToDict(frame)
    if frame_dict in frame_dicts:
      remove_indices.append(index)
    else:
      frame_dicts.append(frame_dict)
    index += 1
  remove_indices.reverse()
  for index in remove_indices:
    print "Removing duplicate %s frame #%d" % (tag.frames[index].header.id, index)
    #tag.frames.removeFrameByIndex(index)  # HAS A BUG
    list.__delitem__(tag.frames, index) #so use this instead
  if remove_indices:
    tag.update()

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
    removeDuplicateId3Frames(fnam)

if __name__ == '__main__':
  main(sys.argv)
