#!/usr/bin/env python2.7
# coding=utf-8

import argparse
import errno
import os
import re
import operator
import subprocess
import sys
import time

from pprint import pprint

"""
Inspired by http://www.reddit.com/r/math/comments/sy52s/prime_factorization_sweater/
"""

# Phiffled hilbert palette.
COLORS = [
  "#605fbf",
  "#dfbf60",
  "#3f9f20",
  "#9fc0df",
  "#ff205f",
  "#1f005f",
  "#00ffbf",
  "#808040",
  "#df40df",
  "#7f1fa0",
  "#df001f",
  "#9fa0ff",
  "#3fe01f",
  "#bf3f80",
  "#602000",
  "#005fdf",
  "#c0df1f",
  "#e0e080",
  "#9f607f",
  "#7f601f",
  "#7fffc0",
  "#7f803f",
  "#801fdf",
  "#205fbf",
  "#c09f1f",
  "#a0c0a0",
  "#20bf5f",
  "#ff7f80",
  "#20bf9f",
  "#a0c060",
  "#206040",
  "#c09fdf",
  "#5f20ff",
  "#802020",
  "#7f80bf",
  "#7fff40",
  "#a06080",
  "#203f1f",
  "#7f60df",
  "#e0df7f",
  "#c0e0e0",
  "#006020",
  "#c03f7f",
  "#3fdfe0",
  "#a0a000",
  "#e000e0",
  "#1f009f",
  "#df401f",
  "#00ff3f",
  "#8080c0",
  "#ff1fa0",
  "#7f1f60",
  "#3f9fe0",
  "#a0c020",
  "#dfbfa0",
  "#804040",
  "#5f5f40",
  "#5fc09f",
  "#5fbf60",
  "#bf5fe0",
  "#5f5f80",
  "#df805f",
  "#80ffbf",
  "#008040",
  "#df405f",
  "#1fdf80",
  "#9fa07f",
  "#df7fe0",
  "#4000c0",
  "#bf3f00",
  "#1f3f60",
  "#5fa0ff",
  "#40df1f",
  "#9f009f",
  "#3f60df",
  "#ffe01f",
  "#3f7f00",
  "#ffffc0",
  "#801f5f",
  "#409f1f",
  "#5fc0df",
  "#bf20df",
  "#3f3f80",
  "#ff7f00",
  "#5f203f",
  "#a0bf9f",
  "#e05fbf",
  "#20c060",
  "#2080a0",
  "#a0ff5f",
  "#ff80bf",
  "#3f20df",
  "#a06000",
  "#407f7f",
  "#60a080",
  "#60df7f",
  "#9f60bf",
  "#400000",
  "#407fbf",
  "#ffbf40",
  "#bfdfe0",
  "#e00060",
  "#20a000",
  "#00e0e0",
  "#9fa03f",
  "#ff40ff",
  "#602080",
  "#ff1f20",
  "#20c020",
  "#bf9fe0",
  "#c020a0",
  "#3f007f",
  "#007fff",
  "#c0ff3f",
  "#dfc09f",
  "#605f3f",
  "#bf5f60",
  "#5fffa0",
  "#5f805f",
  "#803fff",
  "#1f7fa0",
  "#dfa03f",
  "#9fdf80",
  "#1fa07f",
  "#df7f60",
  "#00bfbf",
  "#80c040",
  "#1f405f",
  "#dfa0ff",
  "#7f1fe0",
  "#9f001f",
  "#60a0c0",
  "#7fe01f",
  "#804080",
  "#602040",
  "#605fff",
  "#dfff60",
  "#dfc0df",
  "#bf205f",
  "#1f401f",
  "#3fffc0",
  "#808000",
  "#c01fdf",
  "#201fbf",
  "#e05f3f",
  "#a080a0",
  "#20ff5f",
  "#ff3f80",
  "#202040",
  "#20a0c0",
  "#80df1f",
  "#e0a080",
  "#001fdf",
  "#9f603f",
  "#1fa03f",
  "#7fc0bf",
  "#e09f7f",
  "#7f609f",
  "#a060c0",
  "#7fbf40",
  "#80e0e0",
  "#ff407f",
  "#7f605f",
  "#20ff9f",
  "#a08060",
  "#e060c0",
  "#5f20bf",
  "#c02020",
  "#40ff3f",
  "#7f80ff",
  "#bf1fa0",
  "#002020",
  "#2040e0",
  "#e0c020",
  "#dfffa0",
  "#5f5f00",
  "#803f7f",
  "#7fdfe0",
  "#5fa03f",
  "#a000e0",
  "#1f409f",
  "#e0a000",
  "#80bfbf",
  "#00c040",
  "#df7fa0",
  "#1f7f60",
  "#1f9f80",
  "#9fe07f",
  "#e0a0c0",
  "#3f00ff",
  "#804000",
  "#5fff60",
  "#5f809f",
  "#bf5fa0",
  "#7f1f20",
  "#5f5fc0",
  "#dfc05f",
  "#bfffc0",
  "#008000",
  "#c01f5f",
  "#bf9f20",
  "#1fc0df",
  "#ff20df",
  "#400080",
  "#5f207f",
  "#ff3f00",
  "#a0a0c0",
  "#00df1f",
  "#df009f",
  "#1fa0ff",
  "#bfe01f",
  "#407f3f",
  "#ffc0bf",
  "#a06040",
  "#60e080",
  "#609f7f",
  "#9f60ff",
  "#3f7f80",
  "#ff803f",
  "#208060",
  "#a0ff9f",
  "#e06040",
  "#3f407f",
  "#20c0a0",
  "#a0bf5f",
  "#ff80ff",
  "#6020c0",
  "#bf1f20",
  "#409fdf",
  "#60c020",
  "#8020a0",
  "#3f1f20",
  "#407fff",
  "#ffff40",
  "#ffdfe0",
  "#3f5f20",
  "#a00060",
  "#40e0e0",
  "#60a000",
  "#c03fff",
  "#1f3fa0",
  "#df7f20",
  "#1fe07f",
  "#9f9f80",
  "#df409f",
  "#400040",
  "#0080c0",
  "#80ff3f",
  "#df809f",
  "#1f3fe0",
  "#bf5f20",
  "#605f7f",
  "#5fbfa0",
  "#5fc05f",
  "#8040c0",
  "#000000",
]

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
]

def compute_factorization(n):
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

def main(n):
  factorizations, prime_to_color = compute_factorization(n)
  print'''<html>
<head>
  <title>A Visualization of Factorization</title>
  <style>
    table {
      font-size: 1px;
      width: 1in;
      height: 1in;
      display: inline;
    }
  '''
  print >>sys.stderr, max(prime_to_color.values())
  for prime, color in sorted(prime_to_color.items()):
    print '    .prime_%d { background-color: %s; }' % (prime, COLORS[color])
  print '''  </style>
</head>
<body>
<p>Inpired by this <a href="http://sonderbooks.com/blog/?p=843">Prime Factorization Sweater</a>. Code should be available soon.</p>
<p>Tip: Try adjusting the width of your browser window to see what patterns show up with different numbers of columns.</p>
'''
  for i, factorization in enumerate(factorizations[1:], 1):
    print factorizationToHtml(i, factorization)
  print '''</body>'''

if __name__ == '__main__':
  main(int(sys.argv[1]))
