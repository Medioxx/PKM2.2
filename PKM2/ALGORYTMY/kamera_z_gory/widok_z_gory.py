import cv2
import matplotlib.pyplot as plt
from peakdetect import *
from kmeans import *
import os, json

refresh_rate = 20 #czestotliwosc sprawdzania zajetosci torow
delta = 20
lines_ratio = 0.8

def save_to_json(data,path):
    try:
        with open(path + "/top_camera.json", "w") as top_camera_file:
            top_camera_file.write(json.dumps(data))
    except OSError as err:
        print("Failed to save configuration: {0}".format(err))

    return True


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


def find_rails(lines):
    #wyszukiwanie wiekszych skupisk linii, czyli potencjalnych torow
    max, _ = peakdet(group_lines(lines), delta)
    max = np.asarray(max)

    #odfiltrowanie skupisk linii, ktore nie sa torami
    mu, clusters  = find_centers(max,2)

    if(clusters[0][0][1] > clusters[1][0][1]):
        cluster = 0
    else:
        cluster = 1

    #wyswietlenie odfiltrowanych dnaych, x oznacza wykryty tor
    for i in range(clusters[cluster].__len__()):
        plt.plot(clusters[cluster][i][0],clusters[cluster][i][1], "x")

    plt.show()
    return clusters[cluster]


def find_trains(lines, clusters):
    #szukamy torow
    peaks, _ = peakdet(group_lines(lines), delta/2)

    #struktury przechowujace wykryte tory
    rails = []
    trains_on_rails = {}

    for k in range(0, clusters.__len__()):
        for i in range(0, peaks.__len__()):
            if(abs(clusters[k][0] - peaks[i][0]) < 3):
                #stosunek ilosci lini w chwili obecnej do ilosci linii w chwili poczatkowej
                diff = float(peaks[i][1]) / float(clusters[k][1])
                rails.append(diff)

    #wybranie tych torow na ktorych najprawdopobniej znajduje sie pociag
    for i in range(0, rails.__len__()):
        if(rails[i] < lines_ratio):
            # print("Pociag na torze", i+1)
            # print(rails[i])
            zajety_tor = 'tor'+ str(i+1)
            trains_on_rails.update({zajety_tor : rails[i]})

    print(trains_on_rails)
    file_path = os.getcwd()

    return save_to_json(trains_on_rails,file_path)

def zajetosc_torow(counter, clusters):

    # wykrywanie lini
    edges = cv2.Canny(frame, 50, 250, apertureSize=3)
    minLineLength = 50
    lines = cv2.HoughLinesP(image=edges, rho=1, theta=np.pi / 180, threshold=70, lines=np.array([]),
                            minLineLength=minLineLength, maxLineGap=5)

    #pogrupowanie linii do odpowiednich obszarow obrazu
    group_lines(lines)

    if (counter == refresh_rate):

        if(clusters.__len__() == 0):
            clusters = find_rails(lines)
        else:
            if(find_trains(lines, clusters) != True):
                return

        #wyzerowanie zmiennych
        counter = 0
        for element in range (0, grouped.__len__()):
            grouped[element] = 0


    return counter,clusters


path = os.getcwd() + "\streams\\"
filename = "5.avi"
video = cv2.VideoCapture(path + filename)

grouped = [0] * 100
clusters = []
counter = 0

while(1):
    _, frame = video.read()

    counter, clusters = zajetosc_torow(counter, clusters)
    counter += 1

    cv2.imshow('frame',frame)

    if (cv2.waitKey(10) & 0xFF == ord('q')):
        break
