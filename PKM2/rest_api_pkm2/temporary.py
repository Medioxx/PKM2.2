import numpy as np
import cv2
import time
import requests
import threading
from threading import Thread, Event, ThreadError



url = 'http://192.168.2.1/?action=stream'


stream = requests.get(url, stream=True)
thread_cancelled = False
print("camera initialised")

bytes = b''
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
while not thread_cancelled:
    try:
        bytes += stream.raw.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            #------------------ insert algorythms HERE ------------------
            # Display the resulting frame
            out.write(frame)
            cv2.imshow('Video', frame)
            # ------------------ algorythms end HERE ------------------
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exit(0)
    except ThreadError:
        thread_cancelled = True