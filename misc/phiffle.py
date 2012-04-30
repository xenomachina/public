#!/usr/bin/env python
# coding=utf-8

"""
  Phi + shuffle = "phiffle"

  This is an algorithm for deterministically "shuffling" input by
  using the golden ratio to make elements that used to be close together
  far apart. Some possible uses:

  - Given a set of music tracks that are "sorted" (eg: by
    artist/album/track number) outputs the list reordered for maximum
    variety.

  - Given a list of colors that have been sorted by similarity, produces
    a new list where taking any consecutive sub-sequence will yield a
    set of very different colors.

  An advantage over random shuffling is that this avoids "clumping". The
  obvious disadvantage is that it's completely deterministic. It is,
  however, somewhat "hash like", in that small variations in the input
  (particularly the number of input elements) can yield very different
  outputs, so it may be possible to add a random seed/salt if you need
  some nondeterminism.

  For convenience, this module can be executed as a script, in which
  case the phiffle function will be run on lines from stdin, and sent to
  stdout.

  Thanks to Amit Patel for the original inspiration.
"""

__copyright__ = "Copyright ©2010 Laurence Gonsalves"
__license__ = "GPv2"

import math
import sys

# φ, aka the golden ratio
PHI = (math.sqrt(5) + 1.0) / 2.0 

def phiffle(seq, increment=PHI):
  """
  phiffle(seq[, increment]) -> shuffled sequence

  Returns a copy of the input sequence, but with the elements shuffled.
  By default, this is done using PHI as the increment, though other
  irrational numbers may work as well.
  """
  result = []
  pos = 0.0
  for item in seq:
    index = int(round((len(result) - 1) * pos))
    result.insert(index, item)
    pos = (pos + increment) % 1.0
  return result


def main():
  for line in phiffle([line.rstrip('\n') for line in sys.stdin]):
    print line


if __name__ == '__main__':
  main()
