#!/bin/bash

# Given a bunch of music files (probably on a thumb drive) renames them based
# on their id3 tags so that crufty car audio players will display something
# half-way reasonable.

set -ex

for i; do
  dir="$(dirname "$i")"
  #./reencodeid3.py "$i"
  j="$dir/$(./formatid3.py '%02t-%n · %a.mp3' "$i")"
  [ "$i" == "$j" ] || mv -iv "$i" "$j"
done
