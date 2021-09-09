import cv2
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import threading
import tkinter as tk
from tkinter import messagebox
#import main
import saveData




def holdAlert(videoPath,hodorTime):
    MsgBox = tk.messagebox.askquestion ('Alert','Is there a suspicious activity?',icon = 'warning')
    print(MsgBox)
    if MsgBox == 'yes':
        isApproved= True
    else:
        isApproved=False
    saveData.addNewRow(isApproved,videoPath,hodorTime)
    firstFrame = None
    f = open('contSize.txt' , 'r')
    contSize = int(f.readline())
    f.close()
    print('Contour Size: ' + str(contSize))
    #main.initial(False, contSize)