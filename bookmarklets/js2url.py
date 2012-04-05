#!/usr/bin/env python

import sys
import urllib

sys.stdout.write('javascript:' + urllib.quote(''.join((line for line in
      (line.strip() for line in sys.stdin.readlines())
    if line and not line.startswith('//')))))
sys.stdout.flush()
