
import requests
import cv2
import urllib
import numpy as np
import os


class Camera:
    def __init__(self,host,password,username):
        self.base_url = 'https://{}:{}@{}/axis-cgi/'.format(username, password, host)

    def GetStream(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        cap = cv2.VideoCapture(self.base_url + 'mjpg/video.cgi')
        out = cv2.VideoWriter('output.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
        while True:
            #r = requests.get(self.base_url + 'mjpg/video.cgi')
            ret, frame = cap.read()
            out.write(frame)
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) == 27:
                cap.release()
                out.release()
                exit(0)



#Get environment variables
HOST = os.getenv('AXIS_HOST')
USER = os.getenv('AXIS_USER')
PASS = os.getenv('AXIS_PASS')

cam = Camera('HOST','USER','PASS')
cam.GetStream()
