from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import cv2
import numpy as np
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import requests
import json

# To remove in final step
tel = {'peron': False, 'zajezdnia': False, 'reka': False, 'przeszkody': False, "czerwony": False, 'twarz': False,
       'ruch': False, 'banan': False}


class Okno(QMainWindow):
    def __init__(self):
        # Commuinication
        self.algorithms = {"movement": "False", "depot": "False", "station": "False", "obstacles": "False",
                           "hand": "False", "face": "False", "banana": "False"}
        self.url_get = 'http://127.0.0.1:5000/logs/get_algorithms'
        self.url_set = 'http://127.0.0.1:5000/logs/set_algorithms'

        QMainWindow.__init__(self)
        self.ui = loadUi('PKM_GUI.ui', self)
        self.skutecznosc_load()
        self.ui.button_stream_start.clicked.connect(self.stream_start)
        # self.ui.button_nagranie_start.clicked.connect(self.send_json)
        # self.ui.button_nagranie_start.clicked.connect(self.nagranie_start)
        self.ui.button_program_stop.clicked.connect(self.program_stop)

        self.ui.button_save_skutecznosc.clicked.connect(self.skutecznosc_save)

        oImage = QImage("tlo.png")
        sImage = oImage.scaled(653, 493)
        # sImage = oImage.scaled(QSize(440,440))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.ui.label.setStyleSheet('QLabel {color: white}')
        self.ui.label_2.setStyleSheet('QLabel {color: white}')
        self.ui.label_5.setStyleSheet('QLabel {color: white}')
        self.ui.label_3.setStyleSheet('QLabel {color: white}')
        self.ui.label_4.setStyleSheet('QLabel {color: white}')

        self.ui.detekcja_zajezdnia_checkBox.setStyleSheet('QCheckBox {color: white}')
        self.ui.detekcja_zajezdnia_checkBox.stateChanged.connect(self.send_zajezdnia_json)

        self.ui.detekcja_przeszkody_checkBox.setStyleSheet('QCheckBox  {color: white}')
        self.ui.detekcja_przeszkody_checkBox.stateChanged.connect(self.send_przeszkody_json)

        self.ui.detekcja_twarz_checkBox.setStyleSheet('QCheckBox  {color: white}')
        self.ui.detekcja_twarz_checkBox.stateChanged.connect(self.send_face_json)

        self.ui.detekcja_banan_checkBox.setStyleSheet('QCheckBox  {color: white}')
        self.ui.detekcja_banan_checkBox.stateChanged.connect(self.send_banan_json)

        self.ui.detekcja_perony_checkBox.setStyleSheet('QCheckBox  {color: white}')
        self.ui.detekcja_perony_checkBox.stateChanged.connect(self.send_perony_json)

        self.ui.detekcja_reka_checkBox.setStyleSheet('QCheckBox  {color: white}')
        self.ui.detekcja_reka_checkBox.stateChanged.connect(self.send_reka_json)

        self.ui.detekcja_ruch_checkBox.setStyleSheet('QCheckBox  {color: white}')
        self.ui.detekcja_ruch_checkBox.stateChanged.connect(self.send_ruch_json)

        # Checkbox initialization
        self.set_checkboxes()
        # self.interval()

        self.ui.button_skutecznosc_zajezdnia_dobrze.clicked.connect(self.zajezdnia_zwieksz_skutecznosc)
        self.ui.button_skutecznosc_zajezdnia_zle.clicked.connect(self.zajezdnia_zmniejsz_skutecznosc)

        self.ui.button_skutecznosc_przeszkody_dobrze.clicked.connect(self.przeszkody_zwieksz_skutecznosc)
        self.ui.button_skutecznosc_przeszkody_zle.clicked.connect(self.przeszkody_zmniejsz_skutecznosc)

        self.ui.button_skutecznosc_twarz_dobrze.clicked.connect(self.twarz_zwieksz_skutecznosc)
        self.ui.button_skutecznosc_twarz_zle.clicked.connect(self.twarz_zmniejsz_skutecznosc)

        self.ui.button_skutecznosc_banan_dobrze.clicked.connect(self.banan_zwieksz_skutecznosc)
        self.ui.button_skutecznosc_banan_zle.clicked.connect(self.banan_zmniejsz_skutecznosc)

        self.ui.button_skutecznosc_perony_dobrze.clicked.connect(self.perony_zwieksz_skutecznosc)
        self.ui.button_skutecznosc_perony_zle.clicked.connect(self.perony_zmniejsz_skutecznosc)

        self.ui.button_skutecznosc_reka_dobrze.clicked.connect(self.reka_zwieksz_skutecznosc)
        self.ui.button_skutecznosc_reka_zle.clicked.connect(self.reka_zmniejsz_skutecznosc)

        self.ui.button_skutecznosc_ruch_dobrze.clicked.connect(self.ruch_zwieksz_skutecznosc)
        self.ui.button_skutecznosc_ruch_zle.clicked.connect(self.ruch_zmniejsz_skutecznosc)

        # def kalibruj_start(self):
        #   os.system("python obsluga_kalibratora.py ")

    def program_stop(self):
        sys.exit()

    def stream_start(self):
        filmOrCam = 2
        print("\nStart detekcji na strumieniu: \n")

        # To remove in final step
        if self.ui.detekcja_zajezdnia_checkBox.isChecked():
            tel['zajezdnia'] = True
            print("Detekcja zajezdni aktywna")
        else:
            tel['zajezdnia'] = False

        if self.ui.detekcja_perony_checkBox.isChecked():
            tel['peron'] = True
            print("Detekcja peronow aktywna")
        else:
            tel['peron'] = False

        if self.ui.detekcja_przeszkody_checkBox.isChecked():
            tel['przeszkody'] = True
            print("Detekcja przeszkod aktywna")
        else:
            tel['przeszkody'] = False

        if self.ui.detekcja_twarz_checkBox.isChecked():
            tel['twarz'] = True
            print("Detekcja twarzy aktywna")
        else:
            tel['twarz'] = False

        if self.ui.detekcja_reka_checkBox.isChecked():
            tel['reka'] = True
            print("Detekcja ruchu reka aktywna")
        else:
            tel['reka'] = False

        if self.ui.detekcja_ruch_checkBox.isChecked():
            tel['ruch'] = True
            print("Detekcja ruchu pociagu aktywna")
        else:
            tel['ruch'] = False

        if self.ui.detekcja_banan_checkBox.isChecked():
            tel['banan'] = True
            print("Detekcja banana aktywna")
        else:
            tel['banan'] = False
        # To remove in final step
        os.system("python skryptRozdzielajacy.py " + str(3) + " czysty.avi " + str(tel))

    def nagranie_start(self):
        # self.wczytaj_plik()
        text = self.ui.nagranie_lineEdit.text()
        text2 = " " + text + " "
        # text2= self.wczytaj_plik()
        print(text2)
        filmOrCam = 1
        print("\nStart detekcji na nagraniu: \n")

        # To remove in final step
        if self.ui.detekcja_zajezdnia_checkBox.isChecked():
            tel['zajezdnia'] = True
            print("Detekcja zajezdni aktywna")

        if self.ui.detekcja_perony_checkBox.isChecked():
            tel['peron'] = True
            print("Detekcja peronow aktywna")

        if self.ui.detekcja_przeszkody_checkBox.isChecked():
            tel['przeszkody'] = True
            print("Detekcja przeszkod aktywna")

        if self.ui.detekcja_twarz_checkBox.isChecked():
            tel['twarz'] = True
            print("Detekcja twarzy aktywna")

        if self.ui.detekcja_reka_checkBox.isChecked():
            tel['reka'] = True
            print("Detekcja ruchu reka aktywna")

        if self.ui.detekcja_ruch_checkBox.isChecked():
            tel['ruch'] = True
            print("Detekcja ruchu pociagu aktywna")

        if self.ui.detekcja_banan_checkBox.isChecked():
            tel['banan'] = True
            print("Detekcja banana aktywna")

        # To remove in final step
        os.system("python skryptRozdzielajacy.py " + str(filmOrCam) + text2 + str(tel))
        print(tel)

    # To remove in final step??????
    def wczytaj_plik(self):
        filename = QFileDialog.getOpenFileName(self, None, '',
                                               'Media file(*.mp4 *.wmv *.avi *.3gp *.oog *.mpeg *.mp2 *.wma *.mp3)'
                                               ';;All files(*.*)')
        print(filename[0])
        return filename[0]

    ###################################### JSON Communication #######################################

    # Method, which downloads current dictionary and applies it to local dictionary
    def get_algorithms(self):
        # get response from RestApi
        rest_api_response = requests.get(self.url_get)
        # Convert response to json/dictionary
        rest_api_dictionary = rest_api_response.json()

        self.algorithms["movement"] = rest_api_dictionary['movement']
        self.algorithms["depot"] = rest_api_dictionary['depot']
        self.algorithms["station"] = rest_api_dictionary['station']
        self.algorithms["obstacles"] = rest_api_dictionary['obstacles']
        self.algorithms["hand"] = rest_api_dictionary['hand']
        self.algorithms["face"] = rest_api_dictionary['face']
        self.algorithms["banana"] = rest_api_dictionary['banana']

    # Method which sends JSON to RestApi
    def set_algorithms(self):
        requests.post(self.url_set, json=self.algorithms)

    def send_face_json(self):
        if self.ui.detekcja_twarz_checkBox.isChecked():
            self.algorithms["face"] = "True"
        else:
            self.algorithms["face"] = "False"
        requests.post(self.url_set, json=self.algorithms)
        pass

    def send_zajezdnia_json(self):
        if self.ui.detekcja_zajezdnia_checkBox.isChecked():
            self.algorithms["depot"] = "True"
        else:
            self.algorithms["depot"] = "False"
        requests.post(self.url_set, json=self.algorithms)
        pass

    def send_przeszkody_json(self):
        if self.ui.detekcja_przeszkody_checkBox.isChecked():
            self.algorithms["obstacles"] = "True"
        else:
            self.algorithms["obstacles"] = "False"
        requests.post(self.url_set, json=self.algorithms)
        pass

    def send_banan_json(self):
        if self.ui.detekcja_banan_checkBox.isChecked():
            self.algorithms["banana"] = "True"
        else:
            self.algorithms["banana"] = "False"
        requests.post(self.url_set, json=self.algorithms)
        pass

    def send_perony_json(self):
        if self.ui.detekcja_perony_checkBox.isChecked():
            self.algorithms["station"] = "True"
        else:
            self.algorithms["station"] = "False"
        requests.post(self.url_set, json=self.algorithms)
        pass

    def send_reka_json(self):
        if self.ui.detekcja_reka_checkBox.isChecked():
            self.algorithms["hand"] = "True"
        else:
            self.algorithms["hand"] = "False"
        requests.post(self.url_set, json=self.algorithms)
        pass

    def send_ruch_json(self):
        if self.ui.detekcja_ruch_checkBox.isChecked():
            self.algorithms["movement"] = "True"
        else:
            self.algorithms["movement"] = "False"
        requests.post(self.url_set, json=self.algorithms)
        pass

    #
    def set_checkboxes(self):
        # First, download current dict from RestApi
        self.get_algorithms()

        if self.algorithms["face"] == "True":
            self.ui.detekcja_twarz_checkBox.setChecked(True)
        else:
            self.ui.detekcja_twarz_checkBox.setChecked(False)

        if self.algorithms["depot"] == "True":
            self.ui.detekcja_zajezdnia_checkBox.setChecked(True)
        else:
            self.ui.detekcja_zajezdnia_checkBox.setChecked(False)

        if self.algorithms["obstacles"] == "True":
            self.ui.detekcja_przeszkody_checkBox.setChecked(True)
        else:
            self.ui.detekcja_przeszkody_checkBox.setChecked(False)

        if self.algorithms["banana"] == "True":
            self.ui.detekcja_banan_checkBox.setChecked(True)
        else:
            self.ui.detekcja_banan_checkBox.setChecked(False)

        if self.algorithms["station"] == "True":
            self.ui.detekcja_perony_checkBox.setChecked(True)
        else:
            self.ui.detekcja_perony_checkBox.setChecked(False)

        if self.algorithms["hand"] == "True":
            self.ui.detekcja_reka_checkBox.setChecked(True)
        else:
            self.ui.detekcja_reka_checkBox.setChecked(False)

        if self.algorithms["movement"] == "True":
            self.ui.detekcja_ruch_checkBox.setChecked(True)
        else:
            self.ui.detekcja_ruch_checkBox.setChecked(False)

    def interval(self):
        threading.Timer(1.0, self.interval).start()
        self.set_checkboxes()

    #Zajezdnia skutecznosc
    def zajezdnia_zwieksz_skutecznosc(self):
        self.zajezdnia_dobrze += 1
        self.zajezdnia_skutecznosc = self.zajezdnia_dobrze / (self.zajezdnia_dobrze + self.zajezdnia_zle) * 100
        if self.zajezdnia_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_zajezdnia.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_zajezdnia.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_zajezdnia.display(self.zajezdnia_skutecznosc)
        pass
    def zajezdnia_zmniejsz_skutecznosc(self):
        self.zajezdnia_zle += 1
        self.zajezdnia_skutecznosc = self.zajezdnia_dobrze / (self.zajezdnia_dobrze + self.zajezdnia_zle) * 100
        if self.zajezdnia_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_zajezdnia.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_zajezdnia.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_zajezdnia.display(self.zajezdnia_skutecznosc)
        pass

    #Przeszkody skutecznosc
    def przeszkody_zwieksz_skutecznosc(self):
        self.przeszkody_dobrze += 1
        self.przeszkody_skutecznosc = self.przeszkody_dobrze / (self.przeszkody_dobrze + self.przeszkody_zle) * 100
        if self.przeszkody_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_przeszkody.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_przeszkody.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_przeszkody.display(self.przeszkody_skutecznosc)
        pass
    def przeszkody_zmniejsz_skutecznosc(self):
        self.przeszkody_zle += 1
        self.przeszkody_skutecznosc = self.przeszkody_dobrze / (self.przeszkody_dobrze + self.przeszkody_zle) * 100
        if self.przeszkody_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_przeszkody.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_przeszkody.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_przeszkody.display(self.przeszkody_skutecznosc)
        pass

    #Twarz skutecznosc
    def twarz_zwieksz_skutecznosc(self):
        self.twarz_dobrze += 1
        self.twarz_skutecznosc = self.twarz_dobrze / (self.twarz_dobrze + self.twarz_zle) * 100
        if self.twarz_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_twarz.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_twarz.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_twarz.display(self.twarz_skutecznosc)
        pass
    def twarz_zmniejsz_skutecznosc(self):
        self.twarz_zle += 1
        self.twarz_skutecznosc = self.twarz_dobrze / (self.twarz_dobrze + self.twarz_zle) * 100
        if self.twarz_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_twarz.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_twarz.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_twarz.display(self.twarz_skutecznosc)
        pass

    #Banan skutecznosc
    def banan_zwieksz_skutecznosc(self):
        self.banan_dobrze += 1
        self.banan_skutecznosc = self.banan_dobrze / (self.banan_dobrze + self.banan_zle) * 100
        if self.banan_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_banan.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_banan.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_banan.display(self.banan_skutecznosc)
        pass
    def banan_zmniejsz_skutecznosc(self):
        self.banan_zle += 1
        self.banan_skutecznosc = self.banan_dobrze / (self.banan_dobrze + self.banan_zle) * 100
        if self.banan_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_banan.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_banan.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_banan.display(self.banan_skutecznosc)
        pass

    #Perony skutecznosc
    def perony_zwieksz_skutecznosc(self):
        self.perony_dobrze += 1
        self.perony_skutecznosc = self.perony_dobrze / (self.perony_dobrze + self.perony_zle) * 100
        if self.perony_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_perony.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_perony.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_perony.display(self.perony_skutecznosc)
        pass
    def perony_zmniejsz_skutecznosc(self):
        self.perony_zle += 1
        self.perony_skutecznosc = self.perony_dobrze / (self.perony_dobrze + self.perony_zle) * 100
        if self.perony_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_perony.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_perony.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_perony.display(self.perony_skutecznosc)
        pass

    #Reka skutecznosc
    def reka_zwieksz_skutecznosc(self):
        self.reka_dobrze += 1
        self.reka_skutecznosc = self.reka_dobrze / (self.reka_dobrze + self.reka_zle) * 100
        if self.reka_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_reka.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_reka.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_reka.display(self.reka_skutecznosc)
        pass
    def reka_zmniejsz_skutecznosc(self):
        self.reka_zle += 1
        self.reka_skutecznosc = self.reka_dobrze / (self.reka_dobrze + self.reka_zle) * 100
        if self.reka_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_reka.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_reka.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_reka.display(self.reka_skutecznosc)
        pass

    #Ruch skutecznosc
    def ruch_zwieksz_skutecznosc(self):
        self.ruch_dobrze += 1
        self.ruch_skutecznosc = self.ruch_dobrze / (self.ruch_dobrze + self.ruch_zle) * 100
        if self.ruch_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_ruch.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_ruch.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_ruch.display(self.ruch_skutecznosc)
        pass
    def ruch_zmniejsz_skutecznosc(self):
        self.ruch_zle += 1
        self.ruch_skutecznosc = self.ruch_dobrze / (self.ruch_dobrze + self.ruch_zle) * 100
        if self.ruch_skutecznosc >= 50:
            self.ui.lcd_skutecznosc_ruch.setStyleSheet('QLCDNumber {color: green}')
        else:
            self.ui.lcd_skutecznosc_ruch.setStyleSheet('QLCDNumber {color: red}')
        self.ui.lcd_skutecznosc_ruch.display(self.ruch_skutecznosc)
        pass

    def skutecznosc_save(self):
        self.skutecznosc_dict['zajezdnia_dobrze'] = self.zajezdnia_dobrze
        self.skutecznosc_dict['zajezdnia_zle'] = self.zajezdnia_zle
        self.skutecznosc_dict['zajezdnia_skutecznosc'] = self.zajezdnia_skutecznosc

        self.skutecznosc_dict['przeszkody_zle'] = self.przeszkody_zle
        self.skutecznosc_dict['przeszkody_dobrze'] = self.przeszkody_dobrze
        self.skutecznosc_dict['przeszkody_skutecznosc'] = self.przeszkody_skutecznosc

        self.skutecznosc_dict['twarz_dobrze'] = self.twarz_dobrze
        self.skutecznosc_dict['twarz_zle'] = self.twarz_zle
        self.skutecznosc_dict['twarz_skutecznosc'] = self.twarz_skutecznosc

        self.skutecznosc_dict['banan_dobrze'] = self.banan_dobrze
        self.skutecznosc_dict['banan_zle'] = self.banan_zle
        self.skutecznosc_dict['banan_skutecznosc'] = self.banan_skutecznosc

        self.skutecznosc_dict['perony_dobrze'] = self.perony_dobrze
        self.skutecznosc_dict['perony_zle'] = self.perony_zle
        self.skutecznosc_dict['perony_skutecznosc'] = self.perony_skutecznosc

        self.skutecznosc_dict['reka_dobrze'] = self.reka_dobrze
        self.skutecznosc_dict['reka_zle'] = self.reka_zle
        self.skutecznosc_dict['reka_skutecznosc'] = self.reka_skutecznosc

        self.skutecznosc_dict['ruch_dobrze'] = self.ruch_dobrze
        self.skutecznosc_dict['ruch_zle'] = self.ruch_zle
        self.skutecznosc_dict['ruch_skutecznosc'] = self.ruch_skutecznosc

        with open('skutecznosc.json', 'w') as fp:
            json.dump(self.skutecznosc_dict, fp)

        print(self.skutecznosc_dict)

    def skutecznosc_load(self):
        with open('skutecznosc.json', 'r') as fp:
            self.skutecznosc_dict = json.load(fp)
            self.zajezdnia_dobrze = self.skutecznosc_dict['zajezdnia_dobrze']
            self.zajezdnia_zle = self.skutecznosc_dict['zajezdnia_zle']
            self.zajezdnia_skutecznosc = self.skutecznosc_dict['zajezdnia_skutecznosc']
            if self.zajezdnia_skutecznosc >= 50:
                self.ui.lcd_skutecznosc_zajezdnia.setStyleSheet('QLCDNumber {color: green}')
            else:
                self.ui.lcd_skutecznosc_zajezdnia.setStyleSheet('QLCDNumber {color: red}')
            self.ui.lcd_skutecznosc_zajezdnia.display(self.zajezdnia_skutecznosc)

            self.przeszkody_zle = self.skutecznosc_dict['przeszkody_zle']
            self.przeszkody_dobrze = self.skutecznosc_dict['przeszkody_dobrze']
            self.przeszkody_skutecznosc = self.skutecznosc_dict['przeszkody_skutecznosc']
            if self.przeszkody_skutecznosc >= 50:
                self.ui.lcd_skutecznosc_przeszkody.setStyleSheet('QLCDNumber {color: green}')
            else:
                self.ui.lcd_skutecznosc_przeszkody.setStyleSheet('QLCDNumber {color: red}')
            self.ui.lcd_skutecznosc_przeszkody.display(self.przeszkody_skutecznosc)

            self.twarz_dobrze = self.skutecznosc_dict['twarz_dobrze']
            self.twarz_zle = self.skutecznosc_dict['twarz_zle']
            self.twarz_skutecznosc = self.skutecznosc_dict['twarz_skutecznosc']
            if self.twarz_skutecznosc >= 50:
                self.ui.lcd_skutecznosc_twarz.setStyleSheet('QLCDNumber {color: green}')
            else:
                self.ui.lcd_skutecznosc_twarz.setStyleSheet('QLCDNumber {color: red}')
            self.ui.lcd_skutecznosc_twarz.display(self.twarz_skutecznosc)

            self.banan_dobrze = self.skutecznosc_dict['banan_dobrze']
            self.banan_zle = self.skutecznosc_dict['banan_zle']
            self.banan_skutecznosc = self.skutecznosc_dict['banan_skutecznosc']
            if self.banan_skutecznosc >= 50:
                self.ui.lcd_skutecznosc_banan.setStyleSheet('QLCDNumber {color: green}')
            else:
                self.ui.lcd_skutecznosc_banan.setStyleSheet('QLCDNumber {color: red}')
            self.ui.lcd_skutecznosc_banan.display(self.banan_skutecznosc)

            self.perony_dobrze = self.skutecznosc_dict['perony_dobrze']
            self.perony_zle = self.skutecznosc_dict['perony_zle']
            self.perony_skutecznosc = self.skutecznosc_dict['perony_skutecznosc']
            if self.perony_skutecznosc >= 50:
                self.ui.lcd_skutecznosc_perony.setStyleSheet('QLCDNumber {color: green}')
            else:
                self.ui.lcd_skutecznosc_perony.setStyleSheet('QLCDNumber {color: red}')
            self.ui.lcd_skutecznosc_perony.display(self.perony_skutecznosc)

            self.reka_dobrze = self.skutecznosc_dict['reka_dobrze']
            self.reka_zle = self.skutecznosc_dict['reka_zle']
            self.reka_skutecznosc = self.skutecznosc_dict['reka_skutecznosc']
            if self.reka_skutecznosc >= 50:
                self.ui.lcd_skutecznosc_reka.setStyleSheet('QLCDNumber {color: green}')
            else:
                self.ui.lcd_skutecznosc_reka.setStyleSheet('QLCDNumber {color: red}')
            self.ui.lcd_skutecznosc_reka.display(self.reka_skutecznosc)

            self.ruch_dobrze = self.skutecznosc_dict['ruch_dobrze']
            self.ruch_zle = self.skutecznosc_dict['ruch_zle']
            self.ruch_skutecznosc = self.skutecznosc_dict['ruch_skutecznosc']
            if self.ruch_skutecznosc >= 50:
                self.ui.lcd_skutecznosc_ruch.setStyleSheet('QLCDNumber {color: green}')
            else:
                self.ui.lcd_skutecznosc_ruch.setStyleSheet('QLCDNumber {color: red}')
            self.ui.lcd_skutecznosc_ruch.display(self.ruch_skutecznosc)

            print(self.skutecznosc_dict)


if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    app = Okno()
    app.show()
    app.interval()
    sys.exit(qApp.exec_())
