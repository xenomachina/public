This is where I'll put random scripts and stuff I want to make available
to the public, but which aren't really big enough to have their own
project.

Some things here are likely to be half-baked or minimally tested. I try
to write reasonably portable code, but a lot of this stuff has only been
tested on one platform (usually Linux (Ubuntu) or OS-X with MacPorts).

Use at your own risk.


media/
======
Stuff for dealing with "media" (music, video, photos).

media/dvdrip/dvdrip.py
----------------------
A wrapper script for ripping DVDs. Uses HandbrakeCLI. Currently Mac
only, but probably easy to port to Linux.

media/id3/id3dump.py
--------------------
Dumps all of the ID3 frames to stdout. For debugging ID3 issues.

media/id3/reencodeid3.py
------------------------
Repairs ID3 tags that were incorrectly marked as latin1 when they were
actually UTF-8.

media/id3/removeid3dupes.py
---------------------------
Removes duplicate ID3 frames.
