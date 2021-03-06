facerecog
=========

Proof of Concept Face Recognition in the Cloud

LICENSING:
FaceRecog - Proof of Concept Face Recognition in the Cloud using Picasa and SkyBiometry

Copyright (C) 2013  Dennis Chow dchow[AT]xtecsystems.com.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software Foundation,
Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA

DISCLAIMER: The author takes no responsibility of how anyone else may
use this software. It is intended as a proof of concept for educational
purposes ONLY.

NOTES:
PoC for facial detect and upload to Picasa account
Some things are hard coded because of limitations in modules
e.g. SimpleCV doesn't allow anything but literal strings
ImportNot everything will be checked for exceptions

REQUIREMENTS: (Tested on Windows Python 2.7.3)
SimpleCV Version 1.3 Superpack: http://simplecv.org/download
SkyBiometry Account with NameSpace set to "facetrain": https://www.skybiometry.com/
Picasa Account dropbox album security at "Limited, anyone with the link": https://picasaweb.google.com

ADDITIONAL CREDIT AND REFS:
https://www.skybiometry.com/Documentation
http://simplecv.org/docs/
http://www.daniweb.com/software-development/python/threads/280403/python-photo-uploader-into-picasa

INSTALLATION NOTES:
1. Unpack the contents of the zip into C:\facerecog (For Linux users you'll have to change this path in the code)
2. Install SimpleCV SuperPack; comes with Python and a few other things
3. Get PyPI or Easy_Install just in case you want to install other packages: https://pypi.python.org/pypi/setuptools
4. Install the Google API client: https://code.google.com/p/google-api-python-client/
5. Install the SkyBiometry API client: https://github.com/Liuftvafas/python-face-client

POSSIBLE USES:
1. Instead of printing the values; parse or straight dump to a log file with timestamp and put into Splunk 4.3 for correlation
2. Host your own secure imaging and modify or automate automatic training tagging in batch for a blacklist of faces to recognize from a stream

KNOWN ISSUES:
1. Security: This program does not address security problems within any of the local or external API/Libraries
2. Security: This program does not validate and sanitize input when moving through memory
3. Security: This program is easily fooled by printing a picture of another face during the detection sequence
4. Detection: This program does not address recognition for other than frontal shots
5. Output: JSON output works directly in Splunk 4.3+ however; requires tuning. You can parse JSON yourself with other modules or as a large string
6. Performance: This program will not scale well without proper memory handling and management
