
import requests
import cv2
import urllib
import numpy as np
import os
import time
import datetime
import threading
from threading import Thread, Event, ThreadError

class Camera:   
    def __init__(self,host,password,username,recording_basepath,camera_name):
        self.basepath=recording_basepath
        self.camera_name=camera_name
        self.base_url = 'https://{}:{}@{}/axis-cgi/'.format(username, password, host)
        self.thread_cancelled = False
        self.thread = Thread(target=self.run)
    
    def start(self):
        self.thread.start()
    
    def is_Alive(self):
        return self.thread.isAlive()
      
    def Record(self):
        #Prepare recording path
        path=self.basepath+self.camera_name+'/'+str(datetime.date.today())+'/'
        if not os.path.exists(path):
            os.makedirs(path)
                           
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        cap = cv2.VideoCapture(self.base_url + 'mjpg/video.cgi')
        oldtime = time.time()
        out = cv2.VideoWriter(path+datetime.datetime.now().strftime('%H:%M')+'.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
        
        while True:   
            # check if 1 hour has passed
            if time.time() - oldtime > 3600:
                path=self.basepath+self.camera_name+'/'+str(datetime.date.today())+'/'
                #check if the new path exists (create a new day directory)
                if not os.path.exists(path):
                    os.makedirs(path)              
                oldtime = time.time()
                #Update CV2 with the new path
                out = cv2.VideoWriter(path+datetime.datetime.now().strftime('%H:%M')+'.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))
   
            ret, frame = cap.read()
            out.write(frame)
            #cv2.imshow('Video', frame)

            if cv2.waitKey(1) == 27:
                cap.release()
                out.release()
                exit(0)
    def run(self):
        try:
            self.Record()
        except ThreadError:
            print("Error - ")
        self.thread_cancelled = True


#Get environment variables
HOST = os.getenv('AXIS_HOST')
USER = os.getenv('AXIS_USER')
PASS = os.getenv('AXIS_PASS')

cam = Camera(HOST,PASS,USER,"","CAMERA2")
cam.start()
