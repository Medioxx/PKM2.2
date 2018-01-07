import cv2
import matplotlib.pyplot as plt
from peakdetect import *
from kmeans import *
import os, json
import numpy as np
import requests
from scipy.cluster.vq import kmeans, whiten

refresh_rate = 40 #czestotliwosc sprawdzania zajetosci torow
delta = 20
lines_ratio = 0.8

url_get = 'http://127.0.0.1:5000/tracks/get_tracks'
url_set = 'http://127.0.0.1:5000/tracks/set_tracks'

def save_to_json(data,path):
    '''
    Opis: Zapisuje dane do pliku json
    Zmienne wejściowe: dane do zapisu, lokalizacja zapisywanego pliku
    Zmienne wyjsciowe: True w przypadku poprawnego zapisu
    '''
    try:
        with open(path + "/top_camera.json", "w") as top_camera_file:
            top_camera_file.write(json.dumps(data))
            requests.post(url_set, json=data)
    except OSError as err:
        print("Failed to save configuration: {0}".format(err))

    return True


def group_lines(lines):
    '''
    Opis: Grupuje wykryte linie w zaleznosci od ich wspolrzednej x
    Zmienne wejściowe: wykryte linie w obrazie
    Zmienne wyjsciowe: wektor zawierajacy pogrupowane linie
    '''
    for line in lines:
        x = line[0][0]/12.80
        grouped[int(x)] += 1
    return grouped


def find_rails(lines):
    '''
    Opis: Funcja znajdująca tory na obrazie
    Zmienne wejściowe: wykryte linie w obrazie
    Zmienne wyjsciowe: wektor zawierający wykryte tory
    '''
    #wyszukiwanie wiekszych skupisk linii, czyli potencjalnych torow
    max, _ = peakdet(group_lines(lines), delta)
    max = list(max)
    # max = np.asarray(max)

    # max = whiten(max)

    #odfiltrowanie skupisk linii, ktore nie sa torami
    mu, clusters  = find_centers(max,2)

    # mu, clusters = kmeans(max,2)

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
    '''
    Opis: Funcja znajdująca pociągi na obrazie
    Zmienne wejściowe: wykryte linie w obrazie, wykryte tory
    Zmienne wyjsciowe: wywołanie funckji save_to_json()
    '''
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
    '''
    Opis: Sprawdzam które tory są zajęte
    Zmienne wejściowe: licznik wywołań funkcji, wykryte tory
    Zmienne wyjsciowe: licznik wywołań funkcji, wykryte tory
    '''
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
# video = cv2.VideoCapture(path + filename)
video = cv2.VideoCapture('rtsp://admin:DoTestowania@172.20.16.106/profile1/media.smp')

grouped = [0] * 100
clusters = []
counter = 0

while(True):
    _, frame = video.read()

    counter, clusters = zajetosc_torow(counter, clusters)
    counter += 1

    cv2.imshow('frame',frame)

    if (cv2.waitKey(10) & 0xFF == ord('q')):
        break