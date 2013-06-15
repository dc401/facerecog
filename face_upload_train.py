#!/usr/bin/python

'''
LICENSING:
Copyright (C)  2013  DENNIS CHOW dchowATxtecsystems.com.
Permission is granted to copy, distribute and/or modify this document
under the terms of the GNU Free Documentation License, Version 1.3
or any later version published by the Free Software Foundation;
with no Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.
A copy of the license is included in the section entitled "GNU
Free Documentation License".

DISCLAIMER: The author takes no responsibility of how anyone else may
use this software. It is inteded as a proof of concept for educational
purposes ONLY.

NOTES:
PoC for facial detect and upload to Picasa code
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

'''

from SimpleCV import *
import time, os, dircache, re, glob
import gdata.photos, gdata.photos.service
from face_client import FaceClient

#VARS
googleID = "ENTER YOUR GOOGLEID/PICASA EMAIL HERE"
googlePWD = "ENTER YOUR PASSWORD OR OTP HERE"

skyBiometryAPI_ID = "ENTER YOUR API ID HERE"
skyBiometryAPI_KEY = "ENTER YOUR API KEY HERE"


#Ensure we are in the correct dir
try:
  os.path.isdir("C:/facerecog")
except:
	print "You must extract files and run from 'C:\facerecog'"

#Clear out old temp files
if os.path.exists('face_detect.jpg'):
	os.unlink('face_detect.jpg')

if os.path.exists('debug_detect_log.txt'):
	os.unlink('debug_detect_log.txt')

if os.path.exists('picasa_response.xml'):
	os.unlink('picasa_response.xml')

for jpg in glob.glob('C:/facerecog/images/*.jpg'):
	os.unlink(jpg)
	
#Create images directory
DIR_PATH = os.getcwd()
if not os.path.exists(str(DIR_PATH) + '\images'):
	os.makedirs(DIR_PATH + '\images')

#Capture for 3 seconds
for i in range(0,3):
	#Capture from the first webcam connected to host
	capframe = Camera().getImage()
	#Use already trained haar method of frontal facial detection
	faces = capframe.findHaarFeatures('C:/facerecog/haarcascade_frontalface_alt.xml')
	#Draw a box around coordinates detected face
	try:
		faces.sortColorDistance(Color.RED) [0].draw(Color.RED)
	except:
		print "Your face is either turned or moving too fast. Slow your roll!"
	#Output coordinates in log
	for detect in faces:
		print "Face detection at:" + str(detect.coordinates())
		#with open('debug_detect_log.txt', 'a') as debugDetect:
		#	debugDetect.write(str(detect.coordinates()))

	#debugDetect.close()
	
	capframe.save('face_detect.jpg')
	#sequential file names
	nameCount = str('%d' + '.jpg') %i 
	os.rename('face_detect.jpg', 'C:/facerecog/images/' + nameCount)
	
	time.sleep(1)
'''
Using depreciated API because this is only a PoC 
EOL Date: April 20, 2015 Use at your own risk
Alternative to using your own personal creds is to use OTP generated per application
'''
#Create client object and get a token and authenticate with timeout
auth = gdata.photos.service.PhotosService()
auth.ClientLogin(googleID, googlePWD)

IMAGE_DIR = str(DIR_PATH) + '\images'
captureList = dircache.listdir(IMAGE_DIR)
album_url = '/data/feed/api/user/default/albumid/default'

print captureList

uploadCount = 0
#upload pictures from dir one at a time
for file in captureList:
	#debug later had to hard code this one for some unknown EOL string error
	filename = "C:/facerecog/images/" +file #
	response = auth.InsertPhotoSimple(album_url, file, 'FaceRecog', filename, content_type='image/jpeg')
	uploadCount = uploadCount + 1
	
	#Writing to file instead of passing directly into memory not using buffer	
	with open('picasa_response.xml', 'a') as debugUpload:
		debugUpload.write(str(response))
		#Looking for direct URL images of the detected faces
		'''
		Using regex string searching instead because ElementTree 
		child element attribute does not contain end tag needed for easy parsing
		of direct URL image of face to utilize in face training API
		'''
		xmlFile = open('picasa_response.xml', 'r')
		urls = re.findall('ns0:content src="https://\w+.googleusercontent.com/\S+', xmlFile.read())
		scrubURLa = re.sub('ns0:content src="', '', str(urls))
		scrubURLb = re.sub("[\[|\]|\"|\']", '', str(scrubURLa))
		scrubURLc = re.sub(", ", ',', str(scrubURLb))
		faceDetectURL = scrubURLc
		print faceDetectURL
		client = FaceClient(skyBiometryAPI_ID, skyBiometryAPI_KEY)		

		skyresponse = client.faces_detect(faceDetectURL)
		tids = [photo['tags'][0]['tid'] for photo in skyresponse['photos']]
		
		promptUID = raw_input("Enter a Unique ID to Train Photo: ")
		promptLabel = raw_input("Enter a label to Train Photo: ")
		
		client.tags_save(tids = ',' .join(tids), uid = str(promptUID)+'@facetrain', label = str(promptLabel))
		trainStatus = client.faces_train(str(promptUID)+'@facetrain')

		print trainStatus
		
debugUpload.close()
