#!/bin/bash
#
# Runs gvim, or MacVim on Macs.

if [ $(uname) == Darwin ]; then
  exec mvim "$@"
else
  exec gvim "$@"
fi
