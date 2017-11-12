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

tel = {'peron': False, 'zajezdnia': False, 'reka': False, 'przeszkody': False, "czerwony": False, 'twarz': False,
       'ruch': False, 'banan': False}


class Okno(QMainWindow):
    def __init__(self):
        # Commuinication
        self.algorithms = {"movement" : "False", "depot" : "False", "station" : "False", "obstacles": "False", "hand" : "False", "face" : "False", "banana" : "False"}
        self.url_get = 'http://127.0.0.1:5000/logs/get_algorithms'
        self.url_set = 'http://127.0.0.1:5000/logs/set_algorithms'


        QMainWindow.__init__(self)
        self.ui = loadUi('PKM_GUI.ui', self)
        self.ui.button_stream_start.clicked.connect(self.stream_start)
        #self.ui.button_nagranie_start.clicked.connect(self.send_json)
        #self.ui.button_kalibruj.clicked.connect(self.kalibruj_start)

        #self.ui.button_program_stop.clicked.connect(self.program_stop)
        #self.ui.button_skutecznosc_dobrze.clicked.connect(self.skutecznosc_dobrze)
        #self.ui.button_skutecznosc_zle.clicked.connect(self.skutecznosc_zle)

        oImage = QImage("tlo.png")
        sImage = oImage.scaled(500,500)
        #sImage = oImage.scaled(QSize(440,440))
        palette = QPalette()
        palette.setBrush(10, QBrush(sImage))
        self.setPalette(palette)

        self.ui.label.setStyleSheet('QLabel {color: white}')
        self.ui.label_2.setStyleSheet('QLabel {color: white}')
        self.ui.label_5.setStyleSheet('QLabel {color: white}')
        self.ui.label_3.setStyleSheet('QLabel {color: white}')
        self.ui.label_4.setStyleSheet('QLabel {color: white}')

        self.ui.detekcja_zajezdnia_checkBox.setStyleSheet('QCheckBox {color: white}')
        self.ui.detekcja_przeszkody_checkBox.setStyleSheet('QCheckBox  {color: white}')

        self.ui.detekcja_twarz_checkBox.setStyleSheet('QCheckBox  {color: white}')
        self.ui.detekcja_twarz_checkBox.stateChanged.connect(self.send_face_json)

        self.ui.detekcja_banan_checkBox.setStyleSheet('QCheckBox  {color: white}')
        self.ui.detekcja_perony_checkBox.setStyleSheet('QCheckBox  {color: white}')
        self.ui.detekcja_reka_checkBox.setStyleSheet('QCheckBox  {color: white}')
        self.ui.detekcja_ruch_checkBox.setStyleSheet('QCheckBox  {color: white}')

        # Checkbox initialization
        self.set_checkboxes()
        #self.interval()



    #def kalibruj_start(self):
     #   os.system("python obsluga_kalibratora.py ")

    def program_stop(self):
        sys.exit()


    def stream_start(self):
        filmOrCam = 2
        print("\nStart detekcji na strumieniu: \n")

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

        os.system("python skryptRozdzielajacy.py " + str(3) + " czysty.avi " + str(tel))

    def nagranie_start(self):
        #self.wczytaj_plik()
        text = self.ui.nagranie_lineEdit.text()
        text2 = " " + text + " "
        #text2= self.wczytaj_plik()
        print (text2)
        filmOrCam = 1
        print("\nStart detekcji na nagraniu: \n")

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

        os.system("python skryptRozdzielajacy.py " + str(filmOrCam) + text2 + str(tel))
        print(tel)

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

    #
    def set_checkboxes(self):
        # First, dowload current dict from RestApi
        self.get_algorithms()

        if self.algorithms["face"] == "True":
            self.ui.detekcja_twarz_checkBox.setChecked(True)
        else:
            self.ui.detekcja_twarz_checkBox.setChecked(False)


    def interval(self):
        threading.Timer(1.0, self.interval).start()
        self.set_checkboxes()








if __name__ == '__main__':
    qApp = QApplication(sys.argv)
    app = Okno()
    app.show()
    app.interval()
    sys.exit(qApp.exec_())
