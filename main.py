import cv2
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import threading
import tkinter as tk
from tkinter import messagebox
from imutils.io import TempFile
import alert
import csv 


# construct the argument parser and parse the arguments

def initial(isFirst, contSize):
	print('Warming up the camera')
	global ap 
	ap = argparse.ArgumentParser()
	ap.add_argument("-v", "--video", help="path to the video file")
	ap.add_argument("-a", "--min-area", type=int, default=contSize, help="minimum area size")
	global args 
	args = vars(ap.parse_args())
	# if the video argument is None, then we are reading from webcam
	if args.get("video", None) is None:
		global vs 
		vs = VideoStream(src=0).start()
		time.sleep(2.0)
	# otherwise, we are reading from a video file
	else:
		#global vs 
		vs = cv2.VideoCapture(args["video"])
	# initialize the first frame in the video stream
	if isFirst:
		checker()
	#time.sleep(100)
	# loop over the frames of the video
	
def checker():
	global firstFrame 
	firstFrame = None
	recTime = 99999999999999.0
	rec = False
	name = 0
	W = None
	H = None
	writer = None
	print('Warming up the system')
	while True:
		# grab the current frame and initialize the occupied/unoccupied
		# text
		frame = vs.read()
		frame = frame if args.get("video", None) is None else frame[1]
		text = "Normal"
		
		# if the frame could not be grabbed, then we have reached the end
		# of the video
		if frame is None:
			break
		# resize the frame, convert it to grayscale, and blur it
		frame = imutils.resize(frame, width=500)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray = cv2.GaussianBlur(gray, (21, 21), 0)
		# if the first frame is None, initialize it
		if firstFrame is None:
			firstFrame = gray
			continue
				# compute the absolute difference between the current frame and
		# first frame
		frameDelta = cv2.absdiff(firstFrame, gray)
		thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
		# dilate the thresholded image to fill in holes, then find contours
		# on thresholded image
		thresh = cv2.dilate(thresh, None, iterations=2)
		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = imutils.grab_contours(cnts)
		# loop over the contours
		for c in cnts:
			# if the contour is too small, ignore it
			if cv2.contourArea(c) < args["min_area"]:
				continue
			# compute the bounding box for the contour, draw it on the frame,
			# and update the text
			(x, y, w, h) = cv2.boundingRect(c)
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			text = "Alert"
			if W is None or H is None:
				(H, W) = frame.shape[:2]
			if not rec:
				fourcc = cv2.VideoWriter_fourcc(*"mp4v")
				tempVideo = TempFile(ext=".mp4", basePath="./assets/tempVid/")
				writer = cv2.VideoWriter(tempVideo.path, fourcc, 30, (W, H), True)
				print(tempVideo.path)
				print('record')
				rec = True
				recTime = time.time()
			writer.write(frame)
		f = open('hodorTime.txt' , 'r')
		hodor = int(f.readline())
		f.close()
		if text=="Normal" and rec:
			try:
				writer.release()
				if time.time() - recTime > hodor:
					print('hodor!!')
					alert.holdAlert(tempVideo.path,time.time() - recTime )
				rec = False
				print('released')
				print(time.time() - recTime)
				firstFrame = None
			except:
				print('Warning')
		elif rec and time.time() - recTime > hodor:
			try:
				writer.release()
				print('hodor!!')
				alert.holdAlert(tempVideo.path,time.time() - recTime )
				rec = False
				print('released')
				print(time.time() - recTime)
				firstFrame = None
			except:
				print('Warning')
			
		cv2.putText(frame, "Area Status: {}".format(text), (10, 20),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
			(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		# show the frame and record if the user presses a key
		cv2.imshow("Security Feed", frame)
		cv2.imshow("Thresh", thresh)
		cv2.imshow("Frame Delta", frameDelta)
		key = cv2.waitKey(1) & 0xFF
		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break
# cleanup the camera and close any open windows
#threading.Thread(target=initial()).start
#time.sleep(10)
#threading.Thread(target=checker()).start
#time.sleep(10)
f = open('contSize.txt' , 'r')
contSize = int(f.readline())
f.close()
initial(True, contSize)

vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()