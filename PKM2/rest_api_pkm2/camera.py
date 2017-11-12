# camera.py

import cv2
import requests
import numpy as np

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

    def __del__(self):
        self.video.release()

    def get_frame_aiball(self):
        url = 'https://www.youtube.com/watch?v=XOacA3RYrXk'
        stream = requests.get(url, stream=True)
        bytes = b''
        bytes += stream.raw.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpeg = bytes[a:b + 2]
            bytes = bytes[b + 2:]

            frame = cv2.imdecode(np.fromstring(jpeg, dtype=np.uint8), cv2.IMREAD_COLOR)
        return stream

    def get_frame_webcam(self):
        success, frame = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        return frame