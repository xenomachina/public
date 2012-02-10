This is where I'll put random scripts and stuff I want to make available
to the public, but which aren't really big enough to have their own
project.

Some things here are likely to be half-baked or minimally tested. I try
to write reasonably portable code, but a lot of this stuff has only been
tested on one platform (usually Linux (Ubuntu) or OS-X with MacPorts).

Use at your own risk.


art/
====

Code that makes pretty pictures.

bin/
====

Small scripts I keep in ~/bin/.

cjk/
====

Code for dealing with CJK (Chinese, Japanese and Korean). Mostly
Chinese, actually, as that's what I'm most familiar with.

media/
======
Stuff for dealing with "media" (music, video, photos).

media/dvdrip/dvdrip.py
----------------------
A wrapper script for ripping DVDs. Uses HandbrakeCLI. Currently Mac
only, but probably easy to port to Linux.

media/id3/*
-----------
Scripts for manipulating ID3 tags. These are currently pretty old, and
use `eyeD3` which I've since stopped using. (My newer ID3 scripts all
use Mutagen.)


palm/
=====

PalmOS related utilities.


vim/
====

Vim related stuff. This is mostly a subset of stuff under ~/.viminfo/.
