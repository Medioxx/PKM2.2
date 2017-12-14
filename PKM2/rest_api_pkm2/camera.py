# camera.py

import cv2
import requests
import numpy as np
from threading import Thread, Event, ThreadError

# Class which is used to get a frame from a webcam or from an aiball camera
class Camera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        #self.url = 'http://192.168.2.1/?action=stream'
        #self.stream = requests.get(self.url, stream=True)
        self.thread_cancelled = False
        #self.thread = Thread(target=self.run)

    def __del__(self):
        self.video.release()

    def get_frame_aiball(self):
        bytes = b''
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
        bytes += self.stream.raw.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        jpg = bytes[a:b + 2]
        bytes = bytes[b + 2:]
        frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
        #------------------ insert algorythms HERE ------------------
        # Display the resulting frame
        #out.write(frame)
        #cv2.imshow('Video', frame)
        # ------------------ algorythms end HERE ------------------
        return frame


    def get_frame_webcam(self):

        success, frame = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        return frame