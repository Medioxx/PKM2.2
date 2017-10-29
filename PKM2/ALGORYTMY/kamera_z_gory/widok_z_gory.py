import cv2
import numpy as np
import matplotlib.pyplot as plt
from peakdetect import *


def group_lines(lines):

    for line in lines:
        x = line[0][0]/12.80
        grouped[int(x)] += 1
    return grouped

def find_rails(lines):
    max, min = peakdet(group_lines(lines), 10)

    sum = 0
    for element in max:
        sum += element[1]

    avg = sum/max.__len__()

    new_max = []
    for element in max:
        if(element[1] > avg):
            new_max.append(element)

    plt.plot(new_max, "x")
    plt.show()

    return sum/max.__len__()

def przeszkody(frame, counter):
    tory = []
    subframe=frame
    empty = True

    # wykrywanie lini
    edges = cv2.Canny(subframe, 50, 250, apertureSize=3)
    minLineLength = 50
    numberOfLines = 0
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=70, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=5)
    if lines is None:
        empty = False

    group_lines(lines)

    if (counter == 10):

        for element in grouped:
            if element > 20:
                tory.append(1)

        print(find_rails(lines))


        counter = 0
        for element in range (0, grouped.__len__()):
            grouped[element] = 0


    if (empty):
        a, b, c = lines.shape
        for i in range(a):
            if (abs(lines[i][0][2] - lines[i][0][0]) < 50):
                cv2.line(subframe, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 6,
                         cv2.LINE_8)
            #for j in range(a):
                # cv2.rectangle(subframe,(lines[i][0][0], lines[i][0][1]), ( lines[i][0][2], lines[i][0][3]), (0, 255, 0), 5 )

    return grouped, counter



video = cv2.VideoCapture('C:\Users\Dawid\Desktop\\filmiki\\test1c.avi')
grouped = [0] * 100
counter = 0

while(video.isOpened()):
    _, frame = video.read()

    num_rows, num_cols = frame.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D((num_cols / 2, num_rows / 2), -90, 1)
   # frame = cv2.warpAffine(frame, rotation_matrix, (num_cols, num_rows))

    grouped, counter = przeszkody(frame, counter)
    counter += 1

    cv2.imshow('frame',frame)

    if (cv2.waitKey(10) & 0xFF == ord('q')):
        break