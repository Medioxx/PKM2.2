import cv2
import numpy as np


def przeszkody(frame):
    subframe=frame
    empty = True

    # wykrywanie lini
    edges = cv2.Canny(subframe, 50, 150, apertureSize=3)
    minLineLength = 100
    numberOfLines = 0
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=70, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=5)
    if lines is None:
        empty = False

    if (empty):
        a, b, c = lines.shape
        for i in range(a):
            if (abs(lines[i][0][2] - lines[i][0][0]) < 50):
                cv2.line(subframe, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 6,
                         cv2.LINE_8)
            #for j in range(a):
                # cv2.rectangle(subframe,(lines[i][0][0], lines[i][0][1]), ( lines[i][0][2], lines[i][0][3]), (0, 255, 0), 5 )

    return

video = cv2.VideoCapture('C:\Users\Dawid\Desktop\\filmiki\\test1c.avi')


while(video.isOpened()):
    _, frame = video.read()

    num_rows, num_cols = frame.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((num_cols / 2, num_rows / 2), -90, 1)
   # frame = cv2.warpAffine(frame, rotation_matrix, (num_cols, num_rows))

    przeszkody(frame);

    cv2.imshow('frame',frame)

    if (cv2.waitKey(10) & 0xFF == ord('q')):
        break
