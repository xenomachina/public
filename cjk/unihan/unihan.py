#!/usr/bin/python

import pickle
import re
import sys

"""
When run as an executable, converts Unihan*.txt (filename in argv) into a
set of pickled dicts, one for each character attribute, keyed by Unicode
character.

Unihan*.txt files are available from
ftp://ftp.unicode.org/Public/6.1.0/ucd/Unihan-6.1.0d1.zip
"""

__copyright__ = \
    "Copyright 2010 Laurence Gonsalves <laurence@xenomachina.com>. GNU GPL v2."

def main(argv):
  CODEPOINT_RE = re.compile(r'^U\+([0-9A-F]{4,5})$')
  dicts = {}
  for arg in argv[1:]:
    for line in open(arg):
      if not line.startswith('#'):
        line = line.rstrip();
        codepoint, field, value = line.split('\t')
        m = CODEPOINT_RE.match(codepoint)
        assert m, 'Bad codepoint %s' % codepoint
        codepoint = unichr(int(m.group(1), 16))
        assert field[0] == 'k'
        field = field[1:]
        d = dicts.get(field)
        if d is None:
          dicts[field] = d = {}
        d[codepoint] = value
  for field, d in dicts.items():
    fnam = field + '.pkl'
    print 'Writing %d records to %s...' % (len(d), fnam)
    pickle.dump(d, open(fnam, 'w'))

if __name__ == '__main__':
  main(sys.argv)
