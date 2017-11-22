import cv2
import matplotlib.pyplot as plt
from peakdetect import *
from kmeans import *
import os, json
# from parser import save_to_json


def save_to_json(data,path):
    try:
        print("Saving configuration...")
        with open(path + "/top_camera.json", "w") as top_camera_file:
            top_camera_file.write(json.dumps(data))
        print("Configuration saved.")
    except OSError as err:
        print("Failed to save configuration: {0}".format(err))

    return True

def group_lines(lines):
    for line in lines:
        x = line[0][0]/12.80
        grouped[int(x)] += 1
    return grouped

  
def find_rails(lines, clusters ,avg):
    max, _ = peakdet(group_lines(lines), 20)

    max = np.asarray(max)

    print(np.median(max, axis= 0))

    mu, clusters  = find_centers(max,2)

    if(clusters[0][0][1] > clusters[1][0][1]):
        cluster = 0
    else:
        cluster = 1

    for i in range(clusters[cluster].__len__()):
        plt.plot(clusters[cluster][i][0],clusters[cluster][i][1], "x")

    plt.show()

    return clusters[cluster], avg
def find_trains(lines, clusters, avg):
    peaks, _ = peakdet(group_lines(lines), 10)
    new_peaks = []
    rails = []
    trains_on_rails = {}

    max = 1.00;
    sum = 0.00
    rail = -1
    match = 0.00

    for k in range(0, clusters.__len__()):
        for i in range(0, peaks.__len__()):
            if(abs(clusters[k][0] - peaks[i][0]) < 3):
                # peaks[i][1] = cluster[1] - peaks[i][1]

                diff = float(peaks[i][1]) / float(clusters[k][1])
                sum += diff
                rails.append(diff)

                if(max > diff):
                    max = diff
                    rail = k + 1
                    new_peaks.append(peaks[i])
                break;

    for i in range(0, rails.__len__()):
        if(rails[i] < 0.8):
            # print("Pociag na torze", i+1)
            # print(rails[i])
            zajety_tor = 'tor'+ str(i+1)
            trains_on_rails.update({zajety_tor : rails[i]})

    print(trains_on_rails)
    file_path = os.getcwd()
    save_to_json(trains_on_rails,file_path)

    # plt.plot(max, "x")
    plt.show()

    return

def przeszkody(frame, counter, rails, clusters, avg):
    subframe=frame


    # wykrywanie lini
    edges = cv2.Canny(subframe, 50, 250, apertureSize=3)
    minLineLength = 50
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=70, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=5)

    group_lines(lines)

    if (counter == 20):

        if(clusters.__len__() == 0):
            clusters, avg = find_rails(lines, clusters, avg)
        else:
            find_trains(lines, clusters, avg)

        counter = 0
        for element in range (0, grouped.__len__()):
            grouped[element] = 0

    for element in rails:
        cv2.line(subframe, (int(element * 12.8), 0), (int(element * 12.8), 1024), (0, 0, 255), 6,
                  cv2.LINE_8)

    return grouped, counter, rails, clusters, avg


path = os.getcwd() + "\streams\\"
filename = "5.avi"
video = cv2.VideoCapture(path + filename)

grouped = [0] * 100
rails = []
clusters = []
avg = 0
counter = 0

while(1):
    _, frame = video.read()

    grouped, counter, rails, clusters, avg = przeszkody(frame, counter, rails, clusters, avg)
    counter += 1

    cv2.imshow('frame',frame)

    if (cv2.waitKey(10) & 0xFF == ord('q')):
        break
