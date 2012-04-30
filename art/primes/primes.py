#!/usr/bin/env python2.7
# coding=utf-8

"""
Generates HTML for a prime factorization visualization.

Inspired by:
  http://www.reddit.com/r/math/comments/sy52s/prime_factorization_sweater/
"""

__copyright__ = "Copyright ©2012 Laurence Gonsalves"
__license__ = "GPv2"

import operator
import sys

import scurve # https://github.com/cortesi/scurve.git

from phiffle import phiffle

# TODO: make a function to automatically construct a layout for n cells,
# rather than having them hard-coded like this. (This can handle up to
# 25 cells, so it gets us up to 2**26-1 (67,108,863).)
LAYOUTS = [
  (),
  (1,),
  (2,),
  (1,1,1),
  (2,2),
  (2,1,2),
  (2,2,2),
  (2,3,2),
  (3,2,3),
  (3,3,3),
  (3,2,2,3),
  (3,2,1,2,3),
  (3,3,3,3),
  (3,3,1,3,3),
  (3,3,2,3,3),
  (3,3,3,3,3),
  (3,3,4,3,3),
  (4,3,3,3,4),
  (4,3,4,3,4),
  (4,4,3,4,4),
  (4,4,4,4,4),
  (4,4,5,4,4),
  (4,5,4,5,4),
  (5,4,5,4,5),
  (5,5,4,5,5),
  (5,5,5,5,5),
]

def compute_factorization(n):
  """
  compute_factorization(n) -> factorizations, prime_to_color

  Where factorizations is a tuple of tuples. Each sub-tuple contains the
  prime factors of its index in the outer tuple.

  For example, factorizations[12] == (2, 2, 3)

  Note that element 0 and 1 are empty.

  prime_to_color is a dict that maps from primes to a unique index.
  These indices are "packed". This is handly if you want to have
  per-prime information in an array.
  """
  factorizations = [list(x) for x in [()] * (n + 1)]
  c = 0
  prime_to_color = {}
  for i in range(2, n + 1):
    if not factorizations[i]:
      prime_to_color[i] = c
      c += 1
      for k in range(1, n + 1):
        if i**k > n:
          break
        for j in range(i**k, n + 1, i**k):
          factorizations[j].append(i)
  factorizations = tuple((tuple(factorization) for factorization in factorizations))
  for i in range(1, n+1):
    assert reduce(operator.mul, factorizations[i], 1) == i
  return factorizations, prime_to_color


def htmlFormat(layout):
  product = reduce(operator.mul, layout, 1)
  result = '<table title="%s">'
  for columns in layout:
    colspan = product // columns
    result += '<tr>'
    result += ('<td colspan=%d class="prime_%%d">&nbsp;</td>' % colspan) * columns
    result += '</tr>'
  result += '</table>'
  return result


def factorizationToHtml(i, factorization):
  layout = LAYOUTS[len(factorization)]
  assert sum(layout) == len(factorization)
  format = htmlFormat(layout)
  return format % ((i,) + factorization)

RGB_SIZE = 256**3

def printStylesheet(prime_to_color):
  print'''<style>
    table {
      width: 1in;
      height: 1in;
      display: inline-table;
    }
    '''

  # We want a diverse palette, so evenly divide a Hilbert curve for RGB
  # space.
  num_colors = max(prime_to_color.values()) + 1
  hilbert = scurve.fromSize('hilbert', 3, RGB_SIZE)
  colors = [hilbert[i] for i in range(0, RGB_SIZE, RGB_SIZE // num_colors)]
  # We also want numbers that are close to each other to have very
  # different colors, so phiffle the colors.
  colors = ['#%02x%02x%02x' % (r,g,b) for (r,g,b) in phiffle(colors)]

  for prime, color in sorted(prime_to_color.items()):
    print '    .prime_%d { background-color: %s; }' % (prime, colors[color])
  print '''</style>'''

def main(n):
  factorizations, prime_to_color = compute_factorization(n)
  print'''<!DOCTYPE html>
<html>
<head>
<title>A Visualization of Factorization</title>'''
  printStylesheet(prime_to_color)
  print'''</head>
<body>

<p>Inpired by this <a href="http://sonderbooks.com/blog/?p=843">Prime
Factorization Sweater</a>. Below are the factorizations for 1 through %d.</p>

<p>Code is available
<a href="https://github.com/xenomachina/public/tree/master/art/primes">here</a>.</p>

<p>Tip: Try adjusting the width of your browser window to see what
patterns show up with different numbers of columns.</p>
''' % n
  for i, factorization in enumerate(factorizations[1:], 1):
    print factorizationToHtml(i, factorization)
  print '''</body>'''

if __name__ == '__main__':
  main(int(sys.argv[1]))
